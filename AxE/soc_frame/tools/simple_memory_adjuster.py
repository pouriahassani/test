#!/usr/bin/env python3
"""
Simple Memory Layout Adjuster for AxE SoC

This tool automatically increases memory region sizes when compilation fails
due to memory layout issues. It's a simple and reliable approach.
"""

import os
import sys
import yaml
from pathlib import Path

def load_memory_config(config_file):
    """Load memory configuration from YAML file"""
    with open(config_file, 'r') as f:
        return yaml.safe_load(f)

def save_memory_config(config_file, config):
    """Save memory configuration to YAML file"""
    with open(config_file, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

def increase_memory_sizes(config, increase_factor=1.5):
    """Increase memory sizes by a factor"""
    layout = config['memory_layout']
    
    # Current sizes
    prog_size = layout['program']['size']
    data_size = layout['data']['size'] 
    file_io_size = layout['file_io']['size']
    
    # Convert to int if hex string
    if isinstance(prog_size, str):
        prog_size = int(prog_size, 16)
    if isinstance(data_size, str):
        data_size = int(data_size, 16)
    if isinstance(file_io_size, str):
        file_io_size = int(file_io_size, 16)
    
    # Increase sizes
    new_prog_size = int(prog_size * increase_factor)
    new_data_size = int(data_size * increase_factor)
    new_file_io_size = int(file_io_size * increase_factor)
    
    # Round up to 4KB boundaries
    new_prog_size = ((new_prog_size + 4095) // 4096) * 4096
    new_data_size = ((new_data_size + 4095) // 4096) * 4096
    new_file_io_size = ((new_file_io_size + 4095) // 4096) * 4096
    
    # Check if expanded file_io would overlap with MMIO (starts at 1MB = 0x100000)
    mmio_base = layout['mmio']['base']
    new_file_io_base = new_prog_size + new_data_size
    new_file_io_end = new_file_io_base + new_file_io_size
    
    # If file_io would overlap with MMIO, limit its size
    if new_file_io_end > mmio_base:
        max_file_io_size = mmio_base - new_file_io_base - 4096  # Leave 4KB gap
        if max_file_io_size > 0:
            new_file_io_size = max_file_io_size
        else:
            # If there's no room even for current file_io, we need to shrink program/data
            available_space = mmio_base - 4096  # Total space minus gap
            # Split available space: 70% program, 20% data, 10% file_io
            new_prog_size = int(available_space * 0.7)
            new_data_size = int(available_space * 0.2) 
            new_file_io_size = available_space - new_prog_size - new_data_size - 8192  # Leave gaps
            
            # Round to 4KB boundaries
            new_prog_size = ((new_prog_size) // 4096) * 4096
            new_data_size = ((new_data_size) // 4096) * 4096
            new_file_io_size = ((new_file_io_size) // 4096) * 4096
    
    # Update layout with new sizes
    layout['program']['size'] = new_prog_size
    
    # Adjust base addresses
    layout['data']['base'] = new_prog_size
    layout['data']['size'] = new_data_size
    
    layout['file_io']['base'] = new_prog_size + new_data_size
    layout['file_io']['size'] = new_file_io_size
    
    return {
        'program': {'old': prog_size, 'new': new_prog_size},
        'data': {'old': data_size, 'new': new_data_size},
        'file_io': {'old': file_io_size, 'new': new_file_io_size}
    }

def regenerate_headers():
    """Regenerate memory layout headers"""
    soc_frame_root = Path(__file__).parent.parent
    config_file = soc_frame_root / "config" / "memory_layout.yaml"
    
    cmd = [
        "python3", 
        str(soc_frame_root / "tools" / "memory_layout_validator.py"),
        str(config_file),
        "--output-dir",
        str(soc_frame_root / "generated")
    ]
    
    import subprocess
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0

def main():
    """Main function"""
    soc_frame_root = Path(__file__).parent.parent
    config_file = soc_frame_root / "config" / "memory_layout.yaml"
    
    print("🔧 Simple Memory Layout Adjuster")
    print("=" * 40)
    
    # Load current configuration
    config = load_memory_config(config_file)
    
    # Increase memory sizes
    print("📈 Increasing memory region sizes by 50%...")
    changes = increase_memory_sizes(config)
    
    # Save updated configuration
    save_memory_config(config_file, config)
    
    # Regenerate headers
    print("⚙️  Regenerating memory layout headers...")
    if not regenerate_headers():
        print("❌ Failed to regenerate headers")
        return False
    
    print("✅ Memory layout adjusted successfully!")
    print("📋 Changes made:")
    for region, change in changes.items():
        old_kb = change['old'] // 1024
        new_kb = change['new'] // 1024
        print(f"   {region}: {old_kb}KB → {new_kb}KB")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)