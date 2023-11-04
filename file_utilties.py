import os

from constants import FDM_EXTENSION, SLA_EXTENSION

DIR_NAME = ""
BASE_NAME = ""


def getDir(stl_file: str):
    global DIR_NAME

    if DIR_NAME == "":
        DIR_NAME = os.path.dirname(stl_file)

    return DIR_NAME


def getBaseName(stl_file: str):
    global BASE_NAME

    if BASE_NAME == "":
        BASE_NAME = os.path.splitext(os.path.basename(stl_file))[0]

    return BASE_NAME


def get_fdm_filename(stl_file: str):
    stl_dir = getDir(stl_file)
    stl_base_name = getBaseName(stl_file)
    return os.path.join(stl_dir, f"{stl_base_name}" + FDM_EXTENSION)


def get_sla_filename(stl_file: str):
    stl_dir = getDir(stl_file)
    stl_base_name = getBaseName(stl_file)
    return os.path.join(stl_dir, f"{stl_base_name}" + SLA_EXTENSION)
