import os
import subprocess

from constants import SLA_EXTENSION, FDM_EXTENSION
from file_utilties import getDir, getBaseName, get_fdm_filename, get_sla_filename


def run_slicers(stl_file, fdm_config, sla_config):
    # Check if all files exist
    if not os.path.exists(stl_file) or not os.path.exists(fdm_config) or not os.path.exists(sla_config):
        print("Error: One or more input files do not exist.")
        return

    # Get model info before slicing using Slic3r for FDM
    print("\nSlic3r FDM Model Information:")
    slic3r_fdm_info_command = f'slic3r-console.exe "{stl_file}" --info'
    subprocess.run(slic3r_fdm_info_command, shell=True)

    # Get model info using PrusaSlicer for SLA (without loading a specific config)
    print("\nPrusaSlicer SLA Model Information:")
    prusa_slicer_sla_info_command = f'prusa-slicer-console.exe "{stl_file}" --info'
    subprocess.run(prusa_slicer_sla_info_command, shell=True)

    # Slice STL model using Slic3r with FDM config
    output_fdm_filename = get_fdm_filename(stl_file)
    print("\nSlicing STL model using Slic3r with FDM Config.")
    slic3r_fdm_command = f'slic3r-console.exe "{stl_file}" --load "{fdm_config}" -o {output_fdm_filename}'
    subprocess.run(slic3r_fdm_command, shell=True)
    print("FDM slicing completed.")

    # Slice STL model using PrusaSlicer with SLA config
    output_sla_filename = get_sla_filename(stl_file)
    print("\nSlicing STL model using PrusaSlicer with SLA Config.")
    prusa_slicer_sla_command = f'prusa-slicer-console.exe -g "{stl_file}" --load "{sla_config}" -o {output_sla_filename}'
    subprocess.run(prusa_slicer_sla_command, shell=True)
    print("SLA slicing completed.")


