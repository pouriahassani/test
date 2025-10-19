#!/usr/bin/env python3
"""
AxE Project Path Management Module

This module provides centralized, portable path management for the entire AxE project.
Replaces hardcoded paths with environment variable-based resolution.

Best Practices Implemented:
- Single source of truth for all paths
- Environment variable fallbacks
- Automatic project root detection
- Cross-platform compatibility
- Comprehensive error handling
- Backwards compatibility with existing code

Usage:
    from axe_paths import AXE_PATHS
    config_file = AXE_PATHS.tools / "config.conf"
    system_dir = AXE_PATHS.systems / "2x2_16_priority_input"
"""

import os
import sys
from pathlib import Path
from typing import Dict, Union, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

class AxEPathManager:
    """
    Path management for AxE project
    
    Provides centralized, environment-variable-based path resolution
    with multiple fallback methods for robustness.
    """
    
    def __init__(self):
        self._project_root: Optional[Path] = None
        self._paths: Optional[Dict[str, Path]] = None
        self._initialize_paths()
    
    def _find_project_root(self) -> Path:
        """
        Find AxE project root using multiple detection methods
        
        Priority order:
        1. AXE_ROOT environment variable
        2. SOC_FRAME_ROOT environment variable (parent directory)
        3. Search from current script location
        4. Search from current working directory
        
        Returns:
            Path: Absolute path to AxE project root
            
        Raises:
            RuntimeError: If project root cannot be located
        """
        
        # Method 1: AXE_ROOT environment variable (highest priority)
        if axe_root := os.environ.get('AXE_ROOT'):
            root_path = Path(axe_root).resolve()
            if self._validate_project_root(root_path):
                logger.info(f"Found project root via AXE_ROOT: {root_path}")
                return root_path
            else:
                logger.warning(f"AXE_ROOT points to invalid directory: {root_path}")
        
        # Method 2: SOC_FRAME_ROOT environment variable
        if soc_frame := os.environ.get('SOC_FRAME_ROOT'):
            root_path = Path(soc_frame).parent.resolve()
            if self._validate_project_root(root_path):
                logger.info(f"Found project root via SOC_FRAME_ROOT: {root_path}")
                return root_path
            else:
                logger.warning(f"SOC_FRAME_ROOT parent is invalid: {root_path}")
        
        # Method 3: Search from script location
        script_path = Path(__file__).resolve()
        for parent in [script_path.parent] + list(script_path.parents):
            if self._validate_project_root(parent):
                logger.info(f"Found project root relative to script: {parent}")
                return parent
        
        # Method 4: Search from current working directory
        cwd = Path.cwd()
        for parent in [cwd] + list(cwd.parents):
            if self._validate_project_root(parent):
                logger.info(f"Found project root from working directory: {parent}")
                return parent
        
        # Method 5: Last resort - assume script is in tools directory
        assumed_root = script_path.parent.parent.parent
        if assumed_root.exists():
            logger.warning(f"Using assumed project root (no validation): {assumed_root}")
            return assumed_root
        
        # All methods failed
        raise RuntimeError(
            "Could not locate AxE project root directory.\n"
            "Solutions:\n"
            "1. Set AXE_ROOT environment variable: export AXE_ROOT=/path/to/axe\n"
            "2. Set SOC_FRAME_ROOT environment variable: export SOC_FRAME_ROOT=/path/to/axe/soc_frame\n"
            "3. Run from within the AxE project directory\n"
            "4. Ensure CLAUDE.md exists in project root"
        )
    
    def _validate_project_root(self, path: Path) -> bool:
        """
        Validate that a path is a valid AxE project root
        
        Args:
            path: Path to validate
            
        Returns:
            bool: True if path is valid AxE project root
        """
        if not path.exists() or not path.is_dir():
            return False
        
        # Check for AxE project markers
        markers = [
            'CLAUDE.md',           # Primary marker
            'soc_frame',           # Essential directory
            'soc_frame/tools',     # Tools directory
        ]
        
        for marker in markers:
            if not (path / marker).exists():
                return False
        
        return True
    
    def _initialize_paths(self):
        """Initialize all AxE project paths"""
        
        # Find project root
        self._project_root = self._find_project_root()
        
        # Set up all paths
        self._paths = {
            # Root directories
            'axe_root': self._project_root,
            'soc_frame': self._project_root / 'soc_frame',
            'docs': self._project_root / 'docs',
            
            # SoC framework subdirectories
            'tools': self._project_root / 'soc_frame' / 'tools',
            'systems': self._project_root / 'soc_frame' / 'systems',
            'rtl': self._project_root / 'soc_frame' / 'rtl',
            'sw': self._project_root / 'soc_frame' / 'sw',
            
            # Software subdirectories
            'controllers': self._project_root / 'soc_frame' / 'sw' / 'controller',
            'programs': self._project_root / 'soc_frame' / 'sw' / 'programs',
            'tasks': self._project_root / 'soc_frame' / 'sw' / 'tasks',
            'libs': self._project_root / 'soc_frame' / 'sw' / '_libs',
            
            # Tools subdirectories
            'solar': self._project_root / 'soc_frame' / 'tools' / 'solar',
            'img': self._project_root / 'soc_frame' / 'tools' / 'img',
        }
        
        # Validate critical paths exist
        critical_paths = ['soc_frame', 'tools', 'systems', 'sw']
        for path_name in critical_paths:
            path = self._paths[path_name]
            if not path.exists():
                logger.error(f"Critical path missing: {path}")
                raise RuntimeError(f"AxE project structure incomplete: {path} not found")
        
        logger.info(f"AxE paths initialized successfully from: {self._project_root}")
    
    def __getattr__(self, name: str) -> Path:
        """
        Allow attribute-style access to paths
        
        Usage: AXE_PATHS.tools instead of AXE_PATHS.get_path('tools')
        """
        if self._paths and name in self._paths:
            return self._paths[name]
        raise AttributeError(f"Path '{name}' not found. Available paths: {list(self._paths.keys()) if self._paths else 'None'}")
    
    def get_path(self, name: str) -> Path:
        """
        Get path by name with error handling
        
        Args:
            name: Path name (e.g., 'tools', 'systems', 'programs')
            
        Returns:
            Path: Absolute path object
            
        Raises:
            KeyError: If path name not found
        """
        if self._paths and name in self._paths:
            return self._paths[name]
        
        available = list(self._paths.keys()) if self._paths else []
        raise KeyError(f"Path '{name}' not found. Available: {available}")
    
    def get_legacy_path(self, name: str) -> str:
        """
        Get path as string for backwards compatibility with old code
        
        Args:
            name: Path name
            
        Returns:
            str: Absolute path as string with trailing slash (legacy format)
        """
        path = self.get_path(name)
        return str(path) + "/"
    
    def resolve_config_file(self, config_name: str) -> Path:
        """
        Resolve configuration file path with multiple search locations
        
        Args:
            config_name: Configuration file name (with or without .conf extension)
            
        Returns:
            Path: Resolved configuration file path
            
        Raises:
            FileNotFoundError: If configuration file not found
        """
        # Normalize config name
        if not config_name.endswith('.conf'):
            config_name += '.conf'
        
        # Search locations in priority order
        search_paths = [
            Path(config_name),                    # Current directory
            self.tools / config_name,             # Tools directory
            Path.cwd() / config_name,             # Working directory
        ]
        
        for path in search_paths:
            if path.exists() and path.is_file():
                return path.resolve()
        
        searched = '\n  '.join(str(p) for p in search_paths)
        raise FileNotFoundError(
            f"Configuration file '{config_name}' not found.\n"
            f"Searched locations:\n  {searched}"
        )
    
    def resolve_solar_data(self, filename: str = "final.csv") -> Path:
        """
        Resolve solar data file path
        
        Args:
            filename: Solar data filename
            
        Returns:
            Path: Resolved solar data file path
            
        Raises:
            FileNotFoundError: If solar data file not found
        """
        solar_file = self.solar / filename
        if solar_file.exists():
            return solar_file
        
        raise FileNotFoundError(f"Solar data file not found: {solar_file}")
    
    def get_system_executable(self, system_name: str) -> Path:
        """
        Get path to system executable
        
        Args:
            system_name: Name of the system
            
        Returns:
            Path: Path to Vtop executable
        """
        return self.systems / system_name / "obj_dir" / "Vtop"
    
    def get_memory_hex_path(self) -> Path:
        """
        Get path for memory hex file (used by simulator)
        
        Returns:
            Path: Path where memory hex file should be placed
        """
        return self.soc_frame / "test.hex"
    
    def get_routing_table_path(self, router_id: int, mesh_config: str = "4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol") -> Path:
        """
        Get path to NoC routing table hex file
        
        Args:
            router_id: Router ID (0-based)
            mesh_config: Mesh configuration string
            
        Returns:
            Path: Path to routing table hex file
        """
        routing_table_dir = self.tools / "Routing_Table"
        filename = f"mesh_{mesh_config}_routing_{router_id}.hex"
        return routing_table_dir / filename
    
    def get_routing_tables_dir(self) -> Path:
        """
        Get path to routing tables directory
        
        Returns:
            Path: Path to routing tables directory
        """
        return self.tools / "Routing_Table"
    
    def list_available_routing_tables(self) -> list[Path]:
        """
        List all available routing table files
        
        Returns:
            list[Path]: List of routing table file paths
        """
        routing_dir = self.get_routing_tables_dir()
        if routing_dir.exists():
            return list(routing_dir.glob("mesh_*_routing_*.hex"))
        return []
    
    def validate_environment(self) -> bool:
        """
        Validate that the AxE environment is properly set up
        
        Returns:
            bool: True if environment is valid
        """
        try:
            # Check that all critical paths exist
            critical_paths = ['soc_frame', 'tools', 'systems', 'programs']
            for path_name in critical_paths:
                path = self.get_path(path_name)
                if not path.exists():
                    logger.error(f"Critical path missing: {path}")
                    return False
            
            # Check that essential files exist
            essential_files = [
                self.tools / "defines.py",
                self.tools / "simulator.py",
                self.tools / "run_mpsoc.py",
            ]
            
            for file_path in essential_files:
                if not file_path.exists():
                    logger.error(f"Essential file missing: {file_path}")
                    return False
            
            logger.info("AxE environment validation successful")
            return True
            
        except Exception as e:
            logger.error(f"Environment validation failed: {e}")
            return False
    
    def setup_python_path(self):
        """
        Set up Python path to include AxE tools directory
        
        This ensures all AxE modules can be imported regardless of working directory.
        """
        tools_str = str(self.tools)
        if tools_str not in sys.path:
            sys.path.insert(0, tools_str)
            logger.info(f"Added to Python path: {tools_str}")
    
    def get_environment_info(self) -> Dict[str, str]:
        """
        Get environment information for debugging
        
        Returns:
            Dict[str, str]: Environment information
        """
        return {
            'axe_root': str(self._project_root),
            'python_executable': sys.executable,
            'working_directory': str(Path.cwd()),
            'script_location': str(Path(__file__)),
            'axe_root_env': os.environ.get('AXE_ROOT', 'not set'),
            'soc_frame_env': os.environ.get('SOC_FRAME_ROOT', 'not set'),
            'python_path_includes_tools': str(self.tools) in sys.path,
        }
    
    def __str__(self) -> str:
        """String representation for debugging"""
        if self._paths:
            paths_str = '\n  '.join(f"{k}: {v}" for k, v in self._paths.items())
            return f"AxEPathManager(\n  {paths_str}\n)"
        return "AxEPathManager(not initialized)"


# ============================================================================
# Global instance - Single source of truth for all AxE paths
# ============================================================================

# Initialize the global path manager - NO SILENT FALLBACKS!
try:
    AXE_PATHS = AxEPathManager()
    AXE_PATHS.setup_python_path()
    
    # Backwards compatibility - Legacy constants for existing code
    # These can be gradually phased out as code is modernized
    PATH_CONTROLLERS = AXE_PATHS.get_legacy_path('controllers')
    PATH_PRGS = AXE_PATHS.get_legacy_path('programs')
    PATH_TASKS = AXE_PATHS.get_legacy_path('tasks')
    PATH_SYSS = AXE_PATHS.get_legacy_path('systems')
    
    # Success message for debugging
    logger.info("AxE path management initialized successfully")
    
except Exception as e:
    # NO SILENT FALLBACKS - Show clear error and exit
    from error_handling import print_error
    import os
    from pathlib import Path
    
    cwd = Path.cwd()
    axe_root_env = os.environ.get('AXE_ROOT', 'NOT SET')
    
    print_error(
        title="AxE Path Management Initialization Failed",
        message=f"""Failed to initialize AxE path management system.

Error details: {e}
Current working directory: {cwd}
AXE_ROOT environment variable: {axe_root_env}

This is a critical failure - the AxE project cannot function without proper path management.""",
        solution=f"""1. Set the AXE_ROOT environment variable:
   export AXE_ROOT=/path/to/axe/project

2. Ensure you're in the AxE project directory:
   cd /path/to/axe/project

3. Verify the AxE project structure:
   ls -la  # Should show: CLAUDE.md, soc_frame/, docs/

4. Run the path resolution test:
   python3 test_hex_paths.py

Example:
   export AXE_ROOT=/home/axe/workspace
   cd /home/axe/workspace/soc_frame/tools
   python3 axe_paths.py"""
    )


# ============================================================================
# Convenience functions for common operations
# ============================================================================

def get_axe_root() -> Path:
    """Get AxE project root directory"""
    return AXE_PATHS.axe_root

def get_soc_frame_root() -> Path:
    """Get SoC framework root directory"""
    return AXE_PATHS.soc_frame

def resolve_config(config_name: str) -> Path:
    """Resolve configuration file path"""
    return AXE_PATHS.resolve_config_file(config_name)

def get_system_executable(system_name: str) -> Path:
    """Get system executable path"""
    return AXE_PATHS.get_system_executable(system_name)

def get_memory_hex_path() -> Path:
    """Get memory hex file path"""
    return AXE_PATHS.get_memory_hex_path()

def get_routing_table_path(router_id: int, mesh_config: str = "4RTs_2VCs_8BD_16DW_SepIFRoundRobinAlloc_2RTsPerRow_2RTsPerCol") -> Path:
    """Get NoC routing table hex file path"""
    return AXE_PATHS.get_routing_table_path(router_id, mesh_config)

def get_routing_tables_dir() -> Path:
    """Get routing tables directory path"""
    return AXE_PATHS.get_routing_tables_dir()

def list_available_routing_tables() -> list[Path]:
    """List all available routing table files"""
    return AXE_PATHS.list_available_routing_tables()


# ============================================================================
# Environment validation and setup
# ============================================================================

def validate_axe_environment() -> bool:
    """Validate AxE environment setup"""
    return AXE_PATHS.validate_environment()

def print_environment_info():
    """Print environment information for debugging"""
    info = AXE_PATHS.get_environment_info()
    print("=== AxE Environment Information ===")
    for key, value in info.items():
        print(f"  {key}: {value}")
    print("=" * 35)


# ============================================================================
# Example usage and testing
# ============================================================================

if __name__ == "__main__":
    """
    Example usage and self-test
    Run this module directly to test path resolution
    """
    
    print("AxE Path Management Self-Test")
    print("=" * 40)
    
    try:
        # Test basic functionality
        print(f"✅ AxE Root: {AXE_PATHS.axe_root}")
        print(f"✅ SoC Frame: {AXE_PATHS.soc_frame}")
        print(f"✅ Tools: {AXE_PATHS.tools}")
        print(f"✅ Systems: {AXE_PATHS.systems}")
        
        # Test legacy compatibility
        print(f"✅ Legacy PATH_PRGS: {PATH_PRGS}")
        
        # Test environment validation
        if validate_axe_environment():
            print("✅ Environment validation passed")
        else:
            print("❌ Environment validation failed")
        
        # Test config resolution
        try:
            config_path = resolve_config("_2x2_main")
            print(f"✅ Config resolved: {config_path}")
        except FileNotFoundError as e:
            print(f"⚠️ Config not found: {e}")
        
        print("\nEnvironment Info:")
        print_environment_info()
        
    except Exception as e:
        print(f"❌ Self-test failed: {e}")
        sys.exit(1)