#!/bin/bash

# Create a temporary file with find exclude patterns based on .gitignore
# This is a simplified approach - for complex .gitignore patterns, Option 1 is better

# Clear/create output file
> all_code.txt

# Find all files, excluding common patterns from your .gitignore
find . -type f \
    -not -path '*/\.*' \
    -not -path '*/obj_dir/*' \
    -not -path '*/build/*' \
    -not -path '*/CMakeFiles/*' \
    -not -path '*/__pycache__/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/venv/*' \
    -not -path '*/env/*' \
    -not -path '*/.venv/*' \
    -not -name '*.o' \
    -not -name '*.obj' \
    -not -name '*.so' \
    -not -name '*.exe' \
    -not -name '*.out' \
    -not -name '*.elf' \
    -not -name '*.bin' \
    -not -name '*.hex' \
    -not -name '*.log' \
    -not -name '*.pyc' \
    -not -name '*.pyo' \
    -not -name '*.tmp' \
    -not -name '*.bak' \
    -not -name '*.swp' \
    -not -name '*.swo' \
    -not -name '.DS_Store' \
    -not -name '*.su' \
    -not -name '*.d' \
    -not -name 'CMakeCache.txt' \
    -not -name '_prgs.json' \
    -not -name '_prgs_with_controller.json' \
    -not -name 'shchexbin.json' \
    -print0 | while IFS= read -r -d '' file; do
        echo "=== FILE: $file ===" >> all_code.txt
        cat "$file" >> all_code.txt
        echo -e "\n\n" >> all_code.txt
done

# Generate tree structure excluding the same patterns
tree -I 'obj_dir|build|CMakeFiles|__pycache__|node_modules|venv|env|*.o|*.so|*.exe|*.out|*.elf|*.bin|*.hex|*.log|*.pyc|*.tmp|*.bak|*.swp|.DS_Store|*.su|*.d|CMakeCache.txt' > project_structure.txt
