# This is a sample Python script.
from constants import FDM_EXTENSION
from slicer_script1 import run_slicers
from file_utilties import getDir, get_fdm_filename
from gcode_parser import parse_gcode_file


# Press the green button in the gutter to run the script.
if __name__ == "__main__":
    stl_file = input("Enter path to STL file: ")
    fdm_config = input("Enter path to FDM config file: ")
    sla_config = input("Enter path to SLA config file: ")

    run_slicers(stl_file, fdm_config, sla_config)

    print("from main: ", parse_gcode_file(get_fdm_filename(stl_file)))

