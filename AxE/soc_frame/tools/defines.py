
# ============================================================================
# AxE Project Path Management - Implementation
# ============================================================================
# 
# MODERN APPROACH: Import from centralized path management module
# This replaces hardcoded paths with environment-variable-based resolution
#
try:
    from axe_paths import PATH_CONTROLLERS, PATH_PRGS, PATH_TASKS, PATH_SYSS
    # Path management successfully imported from axe_paths module
except ImportError as e:
    # NO SILENT FALLBACKS - Show clear error and exit
    from error_handling import import_error
    
    import_error(
        module_name="axe_paths",
        import_path=str(__file__)
    )

# arguments for memory packer

MEM_PACKER_OUTPUT_MEMORY = "0"
MEM_PACKER_OUTPUT_DEBUG = "1"


# args for the simulator

SIM_NO_ARGS = None

SIM_PRINT_OUTPUT = True
SIM_RETURN_OUTPUT = False
