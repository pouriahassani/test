  #!/bin/bash

  cd /home/axe/workspace/mibench_axe

  echo "=== MiBench-AxE Setup Script ==="
  echo "This will clone AxE for all 27 MiBench applications..."
  echo "This may take 15-20 minutes to complete."
  echo ""

  # Define the MiBench applications structure
  declare -A MIBENCH_APPS
  MIBENCH_APPS[automotive]="basicmath bitcount qsort susan"
  MIBENCH_APPS[consumer]="jpeg lame mad tiff2bw tiff2rgba tiffdither tiffmedian typeset"
  MIBENCH_APPS[network]="dijkstra patricia"
  MIBENCH_APPS[office]="ghostscript ispell rsynth sphinx stringsearch"
  MIBENCH_APPS[security]="blowfish pgp rijndael sha"
  MIBENCH_APPS[telecomm]="CRC32 FFT adpcm gsm"

  # Clone AxE for all applications
  total_apps=0
  completed_apps=0

  for category in "${!MIBENCH_APPS[@]}"; do
      for app in ${MIBENCH_APPS[$category]}; do
          total_apps=$((total_apps + 1))
      done
  done

  echo "Total applications to process: $total_apps"
  echo ""

  for category in "${!MIBENCH_APPS[@]}"; do
      echo "Processing category: $category"

      for app in ${MIBENCH_APPS[$category]}; do
          app_dir="$category/$app"
          completed_apps=$((completed_apps + 1))

          echo "  [$completed_apps/$total_apps] Processing: $app_dir"

          if [ ! -d "$app_dir/axe" ]; then
              cd "$app_dir"
              echo "    → Cloning AxE..."
              if git clone -b clean https://github.com/EclectX/AxE.git axe > /dev/null 2>&1; then
                  echo "    ✓ AxE cloned successfully"

                  # Copy project files from our current workspace
                  echo "    → Copying project files..."

                  # Copy our enhanced files to the cloned AxE
                  cp -r /home/axe/workspace/soc_frame/sw/_libs/* axe/soc_frame/sw/_libs/
                  cp -r /home/axe/workspace/soc_frame/config/* axe/soc_frame/config/
                  mkdir -p axe/soc_frame/generated
                  cp -r /home/axe/workspace/soc_frame/generated/* axe/soc_frame/generated/ 2>/dev/null || echo "    (No generated files to copy)"

                  # Copy the specific MiBench application
                  echo "    → Setting up MiBench application..."
                  rm -rf axe/soc_frame/sw/programs/*
                  cp -r /home/axe/workspace/soc_frame/sw/programs/mibench/$category/$app axe/soc_frame/sw/programs/

                  # Create a simple launch script
 