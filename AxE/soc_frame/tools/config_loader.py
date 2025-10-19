"""
AxE Configuration Loader

Configuration loading system for AxE with YAML support,
error handling and validation.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Dict, Any, Tuple, Union, List, Optional


def load_config(config_filename: str) -> Tuple[Dict[str, Any], str]:
    """
    Load and validate AxE YAML configuration file
    
    Args:
        config_filename: Config file name (supports .yaml, .yml extensions)
        
    Returns:
        tuple: (config_dict, base_filename_for_output)
        
    Raises:
        FileNotFoundError: If configuration file not found
        ImportError: If PyYAML not available
        ValueError: If required sections missing
    """
    logging.info(f"Loading configuration: {config_filename}")
    
    # Determine file path
    config_path = None
    
    # Try YAML formats
    yaml_variants = [
        config_filename + '.yaml',
        config_filename + '.yml'
    ]
    
    # First try with axe_paths if available
    try:
        from axe_paths import AXE_PATHS
        
        for variant in yaml_variants:
            try:
                resolved_path = AXE_PATHS.resolve_config_file(variant)
                if resolved_path.exists():
                    config_path = resolved_path
                    logging.info(f"Found config: {config_path}")
                    break
            except (FileNotFoundError, AttributeError):
                continue
                
    except ImportError as e:
        # Show warning for import failure but continue with fallback
        from error_handling import print_warning
        
        print_warning(
            title="AxE Path Management Not Available",
            message=f"Cannot import axe_paths module: {e}",
            suggestion="Using direct file access as fallback. For better path management, ensure axe_paths.py is available."
        )
    
    # Fallback to direct file access
    if config_path is None:
        for test_file in yaml_variants:
            if os.path.exists(test_file):
                config_path = test_file
                logging.info(f"Found config: {config_path}")
                break
    
    if config_path is None:
        raise FileNotFoundError(f"YAML configuration file not found: {config_filename} (tried .yaml, .yml)")
    
    # Load YAML configuration
    config_dict = load_yaml_config(config_path)
    
    # Extract base filename for output files
    base_name = os.path.splitext(os.path.basename(config_filename))[0]
    
    logging.info(f"Config loaded. Base name: {base_name}")
    return config_dict, base_name


def load_yaml_config(config_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load YAML configuration file with validation
    
    Args:
        config_path: Path to YAML configuration file
        
    Returns:
        Dictionary containing configuration data
        
    Raises:
        ImportError: If PyYAML not available
        ValueError: If required sections missing
    """
    try:
        import yaml
    except ImportError:
        raise ImportError("PyYAML not installed. Install with: pip install PyYAML")
    
    with open(config_path, 'r') as f:
        config_dict = yaml.safe_load(f)
    
    # Validate required sections exist
    required_sections = ['controller', 'system', 'run', 'simulation']
    missing_sections = [sec for sec in required_sections if sec not in config_dict]
    
    if missing_sections:
        raise ValueError(f"YAML config missing required sections: {missing_sections}")
    
    return config_dict


def get_config_value(config: Dict[str, Any], yaml_key_path: str, value_type: str = 'string', 
                    required: bool = True, default: Any = None) -> Any:
    """
    Safely extract configuration values from YAML config with type conversion and validation
    
    Args:
        config: Config dictionary (YAML format)
        yaml_key_path: Nested key path (e.g., 'controller.name')
        value_type: 'string', 'int', 'float', 'bool', 'list'
        required: Whether the key is required
        default: Default value if key is missing and not required
        
    Returns:
        Extracted and converted configuration value
        
    Raises:
        ValueError: If required key missing or type conversion fails
    """
    try:
        # Navigate nested dictionary
        keys = yaml_key_path.split('.')
        current = config
        
        for k in keys:
            if isinstance(current, dict) and k in current:
                current = current[k]
            else:
                if required:
                    raise ValueError(f"Required key path '{yaml_key_path}' not found in YAML config")
                return default
        
        value = current
        
        # Type conversion
        if value_type == 'string':
            return str(value).strip() if value is not None else default
        elif value_type == 'int':
            return int(value) if value is not None else default
        elif value_type == 'float':
            return float(value) if value is not None else default
        elif value_type == 'bool':
            if isinstance(value, bool):
                return value
            return str(value).lower() in ('true', '1', 'yes', 'on') if value is not None else default
        elif value_type == 'list':
            if isinstance(value, list):
                return value
            elif isinstance(value, str):
                # Split by comma and clean up
                return [item.strip() for item in value.split(',') if item.strip()]
            else:
                return default if default is not None else []
        else:
            raise ValueError(f"Unsupported value_type: {value_type}")
            
    except Exception as e:
        print(f"Config error in {yaml_key_path}: {e}")
        if required:
            sys.exit(1)
        return default


def extract_controller_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract controller configuration section
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        Dictionary with controller settings
    """
    return {
        'name': get_config_value(config, "controller.name"),
        'save_mode_at': get_config_value(config, "controller.save_mode_at", "int"),
        'start_charging_at': get_config_value(config, "controller.start_charging_at", "int"),
        'stop_charging_at': get_config_value(config, "controller.stop_charging_at", "int"),
    }


def extract_system_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract system configuration section
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        Dictionary with system settings
    """
    return {
        'name': get_config_value(config, "system.name"),
        'architectures': get_config_value(config, "system.architectures", "list"),
        'node_architectures': get_config_value(config, "system.node_architectures", "list"),
    }


def extract_run_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract run configuration section
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        Dictionary with run settings
    """
    return {
        'mode': get_config_value(config, "run.mode"),
        'exec_interval_modifier': get_config_value(config, "run.exec_interval_modifier", "float"),
    }


def extract_simulation_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract simulation configuration section
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        Dictionary with simulation settings
    """
    return {
        'arguments': get_config_value(config, "simulation.arguments", "list"),
        'print_output': get_config_value(config, "simulation.print_output", "bool"),
    }


def extract_programs_config(config: Dict[str, Any]) -> Optional[List[str]]:
    """
    Extract programs configuration section (if run.mode = prgs)
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        List of program names or None if not in programs mode
    """
    run_mode = get_config_value(config, "run.mode")
    if run_mode == "prgs":
        return get_config_value(config, "programs.program_list", "list")
    return None


def extract_tasks_config(config: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Extract tasks configuration section (if run.mode = tasks)
    
    Args:
        config: Full configuration dictionary
        
    Returns:
        Dictionary with task generation settings or None if not in tasks mode
    """
    run_mode = get_config_value(config, "run.mode")
    if run_mode == "tasks":
        return {
            'count': get_config_value(config, "tasks.count", "int"),
            'loop_count_min': get_config_value(config, "tasks.loop_count.min", "int"),
            'loop_count_max': get_config_value(config, "tasks.loop_count.max", "int"),
            'percent_mul_min': get_config_value(config, "tasks.multiplication_percentage.min", "int"),
            'percent_mul_max': get_config_value(config, "tasks.multiplication_percentage.max", "int"),
        }
    return None


def load_complete_config(config_filename: str) -> Dict[str, Any]:
    """
    Load complete configuration with all sections extracted and validated
    
    Args:
        config_filename: Config file name
        
    Returns:
        Dictionary with structured configuration data
    """
    config_dict, base_name = load_config(config_filename)
    
    # Extract all configuration sections
    complete_config = {
        'base_name': base_name,
        'controller': extract_controller_config(config_dict),
        'system': extract_system_config(config_dict),
        'run': extract_run_config(config_dict),
        'simulation': extract_simulation_config(config_dict),
    }
    
    # Add conditional sections based on run mode
    programs = extract_programs_config(config_dict)
    if programs:
        complete_config['programs'] = programs
        
    tasks = extract_tasks_config(config_dict)
    if tasks:
        complete_config['tasks'] = tasks
    
    return complete_config


def print_config_summary(config: Dict[str, Any]) -> None:
    """
    Print a formatted summary of loaded configuration
    
    Args:
        config: Complete configuration dictionary
    """
    print(f"✅ Configuration loaded:")
    print(f"   Controller: {config['controller']['name']}")
    print(f"   System: {config['system']['name']}")
    print(f"   Architectures: {config['system']['architectures']}")
    print(f"   Node architectures: {config['system']['node_architectures']}")
    print(f"   Run mode: {config['run']['mode']}")
    
    if 'programs' in config:
        print(f"   Programs: {config['programs']}")
    elif 'tasks' in config:
        print(f"   Task count: {config['tasks']['count']}")


# Example usage and testing
if __name__ == "__main__":
    # Test configuration loading
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
        try:
            config = load_complete_config(config_file)
            print_config_summary(config)
        except Exception as e:
            print(f"Configuration loading failed: {e}")
            sys.exit(1)
    else:
        print("Usage: python config_loader.py <config_filename>")