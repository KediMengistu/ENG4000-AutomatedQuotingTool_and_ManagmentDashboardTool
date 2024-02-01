import os
import subprocess
from slicerScript2 import mass_retrieval
from tweaker3 import Tweaker

# Function to prompt user for 3D model file path
def get_model_file_path():
    """
    Prompts the user for the path of the 3D model file.
    Returns:
        str: Path to the 3D model file.
    """
    return input("Enter the path of the 3D model file: ")


# Function to prompt user for Print Configurations file path
def get_print_config_file_path():
    """
    Prompts the user for the path of the print configuration file.
    Returns:
        str: Path to the print configuration file.
    """
    return input("Enter the path of the print configuration file: ")


# Function to parse the print configuration file
def create_print_parameters_dict(config_file_path):
    """
    Parses the print configuration file and creates a dictionary of print parameters.
    Args:
        config_file_path (str): Path to the print configuration file.
    Returns:
        dict: Dictionary containing print parameters.
    """
    print_parameters = {}
    with open(config_file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            print_parameters[key.strip()] = value.strip()
    return print_parameters


# Function to extract model information and redirect output to a file
def extract_model_info(model_file_path):
    """
    Extracts information about the model and redirects output to a text file.
    Args:
        model_file_path (str): Path to the 3D model file.
    Returns:
        str: Path to the created information text file.
    """
    output_info_dir = "C:\\Users\\KediM\\OneDrive\\Desktop\\ScriptInfoOutput"
    os.makedirs(output_info_dir, exist_ok=True)

    input_file_base_name = os.path.splitext(os.path.basename(model_file_path))[0]
    output_info_path = os.path.join(output_info_dir, f"{input_file_base_name}_info.txt")

    info_command = f"prusa-slicer-console.exe --info \"{model_file_path}\""
    with open(output_info_path, "w") as file:
        subprocess.run(info_command, shell=True, stdout=file)

    return output_info_path


# Function to create configuration file from dictionary and return its path
def create_config_file(print_parameters, model_file_path):
    """
    Creates a configuration file from print parameters dictionary.
    Args:
        print_parameters (dict): Dictionary of print parameters.
        model_file_path (str): Path to the 3D model file.
    Returns:
        str: Full path of the newly created configuration file.
    """
    config_dir = "C:\\Users\\KediM\\OneDrive\\Desktop\\Config"
    os.makedirs(config_dir, exist_ok=True)

    model_name = os.path.splitext(os.path.basename(model_file_path))[0]
    config_file_name = f"{model_name}_config.ini"
    config_file_path = os.path.join(config_dir, config_file_name)

    config_command = "prusa-slicer-console.exe"
    for key, value in print_parameters.items():
        config_command += f" --{key} {value}"
    config_command += f" --save \"{config_file_path}\""

    subprocess.run(config_command, shell=True)

    return config_file_path


# Function to execute slicing of the model and return paths to G-code and slice info files
def execute_slicing(config_file_path, model_file_path):
    """
    Executes the slicing of the model and returns paths to the G-code and slice info files.
    Args:
        config_file_path (str): Path to the configuration file.
        model_file_path (str): Path to the 3D model file.
    Returns:
        list: [Path to the G-code file, Path to the slice info text file]
    """
    gcode_output_dir = "C:\\Users\\KediM\\OneDrive\\Desktop\\ScriptGcodeOutput"
    slice_info_output_dir = "C:\\Users\\KediM\\OneDrive\\Desktop\\ScriptSliceInfoOutput"
    os.makedirs(gcode_output_dir, exist_ok=True)
    os.makedirs(slice_info_output_dir, exist_ok=True)

    model_name = os.path.splitext(os.path.basename(model_file_path))[0]
    gcode_file_path = os.path.join(gcode_output_dir, f"{model_name}.gcode")
    slice_info_file_path = os.path.join(slice_info_output_dir, f"{model_name}_slice_info.txt")

    slicing_command = f"prusa-slicer-console.exe -g \"{model_file_path}\" --load \"{config_file_path}\" --output \"{gcode_file_path}\""
    with open(slice_info_file_path, "w") as file:
        subprocess.run(slicing_command, shell=True, stdout=file, stderr=subprocess.STDOUT)

    return [gcode_file_path, slice_info_file_path]


# Function to check if the G-code file exists
def check_gcode_file_exists(gcode_file_path):
    """
    Checks if the G-code file exists at the given path.
    Args:
        gcode_file_path (str): Path to the G-code file.
    Returns:
        bool: True if the file exists, False otherwise.
    """
    return os.path.exists(gcode_file_path)


# Function to handle G-code file not existing
def handle_gcode_generation_issue(model_file_path, print_parameters):
    """
    Handles the issue when G-code file does not exist by scaling the model and overwriting the original file.
    Args:
        model_file_path (str): Path to the model file.
        print_parameters (dict): Dictionary of print parameters.
    """
    print("G-code file not generated.")
    print("Please choose an action:")
    print("(1) Scale up model\n(2) Scale down model\n(3) Scale from centimeters to mm\n(4) Scale from inches to mm\n(Any other key to exit)")
    choice = input("Enter your choice: ")

    # Determine the scale factor based on user choice
    scale_factor = ''
    if choice == '1':
        scale_factor = input("Enter scale percentage to enlarge model: ") + '%'
    elif choice == '2':
        scale_factor = input("Enter scale percentage to reduce model: ") + '%'
    elif choice == '3':
        scale_factor = '1000%'  # Scale from centimeters to mm
    elif choice == '4':
        scale_factor = '2540%'  # Scale from inches to mm
    else:
        print("Terminating program.")
        exit(0)

    # Extract file type from model file path
    file_type = os.path.splitext(model_file_path)[1].replace('.', '')

    # Construct and execute the scale command
    scale_command = f"prusa-slicer-console.exe --export-{file_type} --scale {scale_factor} \"{model_file_path}\" --output \"{model_file_path}\""
    subprocess.run(scale_command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    # Update the print parameters with the new scale factor
    # print_parameters['scale'] = scale_factor


# Main execution
# def main():
#     model_file_path = get_model_file_path()
#     config_file_path = get_print_config_file_path()
#
#     print_parameters = create_print_parameters_dict(config_file_path)
#     model_info_path = extract_model_info(model_file_path)
#
#     config_file_created_path = create_config_file(print_parameters, model_file_path)
#     gcode_file_path, slice_info_file_path = execute_slicing(config_file_created_path, model_file_path)
#
#     # In the main function, update the call like this:
#     while not check_gcode_file_exists(gcode_file_path):
#         handle_gcode_generation_issue(model_file_path, print_parameters)
#         model_info_path = extract_model_info(model_file_path)
#         config_file_created_path = create_config_file(print_parameters, model_file_path)
#         gcode_file_path, slice_info_file_path = execute_slicing(config_file_created_path, model_file_path)
#
#
#
#     # Call to mass_retrieval function from slicerScript2
#     mass_retrieval(model_info_path, slice_info_file_path, gcode_file_path)


def main():
    model_file_path = get_model_file_path()
    config_file_path = get_print_config_file_path()

    # Use Tweaker-3 to find the optimal orientation
    # The following command assumes Tweaker outputs the optimized model to a new file
    tweaked_model_file_path = os.path.splitext(model_file_path)[0] + "_tweaked.stl"
    tweaker_command = f"\"C:\\Users\\KediM\\PycharmProjects\\pythonProject\\.venv\\Scripts\\python.exe\" \"C:\\Users\\KediM\\PycharmProjects\\pythonProject\\.venv\\Lib\\site-packages\\tweaker3\\Tweaker.py\" -i \"{model_file_path}\" -o \"{tweaked_model_file_path}\" -vb -x"
    subprocess.run(tweaker_command, shell=True)

    # Continue with the rest of your script using the tweaked model file
    print_parameters = create_print_parameters_dict(config_file_path)
    model_info_path = extract_model_info(tweaked_model_file_path)

    config_file_created_path = create_config_file(print_parameters, tweaked_model_file_path)
    gcode_file_path, slice_info_file_path = execute_slicing(config_file_created_path, tweaked_model_file_path)

    while not check_gcode_file_exists(gcode_file_path):
        handle_gcode_generation_issue(tweaked_model_file_path, print_parameters)
        model_info_path = extract_model_info(tweaked_model_file_path)
        config_file_created_path = create_config_file(print_parameters, tweaked_model_file_path)
        gcode_file_path, slice_info_file_path = execute_slicing(config_file_created_path, tweaked_model_file_path)

    # Call to mass_retrieval function
    mass_retrieval(model_info_path, slice_info_file_path, gcode_file_path)

if __name__ == "__main__":
    main()