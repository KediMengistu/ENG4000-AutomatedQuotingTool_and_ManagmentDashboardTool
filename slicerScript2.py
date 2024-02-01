class Model_Mass_Calc_Info:
    def __init__(self, info_dict, gcode_dict):
        self.size_x = float(info_dict.get('size_x', 0)) / 10
        self.size_y = float(info_dict.get('size_y', 0)) / 10
        self.size_z = float(info_dict.get('size_z', 0)) / 10
        self.box_volume = float(info_dict.get('volume', 0)) / 1000

        self.filament_type = gcode_dict.get('filament_type', "")
        self.filament_density = float(gcode_dict.get('filament_density', 0))
        self.filament_diameter = float(gcode_dict.get('filament_diameter', 0)) / 10
        self.infill_density = float(gcode_dict.get('fill_density', '0%').rstrip('%')) / 100
        self.filament_length = float(gcode_dict.get('filament used [mm]', 0)) / 10
        self.filament_volume = float(gcode_dict.get('filament used [cm3]', 0))
        self.gcode_mass = float(gcode_dict.get('filament used [g]', 0))
        self.calculated_mass = 0

    def calculate_mass(self):
        self.calculated_mass = self.filament_volume * self.filament_density
        return self.calculated_mass

# Function to read the info file and return a dictionary
def read_info_file(info_file_path):
    with open(info_file_path, 'r') as file:
        lines = file.readlines()
        info_dict = {line.split('=')[0].strip(): line.split('=')[1].strip() for line in lines[1:]}
        info_dict['model_name'] = lines[0].strip('[]\n')
    return info_dict

# Function to check the slice info file for print stability warning
def check_slice_info_for_supports(slice_info_file_path):
    with open(slice_info_file_path, 'r') as file:
        if "print warning: Detected print stability issues:" in file.read():
            return "Supports required for print"
    return ""

# Function to read the gcode file and return a dictionary
def read_gcode_file(gcode_file_path):
    gcode_dict = {}
    with open(gcode_file_path, 'r') as file:
        for line in file:
            if line.startswith(';') and '=' in line:
                key, value = line.lstrip('; ').split('=', 1)
                gcode_dict[key.strip()] = value.strip()
    return gcode_dict

def mass_retrieval(info_file_path, slice_info_file_path, gcode_file_path):
    info_dict = read_info_file(info_file_path)
    supports_required_message = check_slice_info_for_supports(slice_info_file_path)
    if supports_required_message:
        print(supports_required_message)
    gcode_dict = read_gcode_file(gcode_file_path)

    model_info = Model_Mass_Calc_Info(info_dict, gcode_dict)
    calculated_mass = model_info.calculate_mass()

    # Print the calculated mass and the mass from G-code (if available)
    print(f"The calculated mass of the model is {calculated_mass:.2f} grams")
    if model_info.gcode_mass > 0:
        print(f"The mass from G-code is {model_info.gcode_mass:.2f} grams")
