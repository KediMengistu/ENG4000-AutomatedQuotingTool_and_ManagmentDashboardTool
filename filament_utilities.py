import math


def calculate_filament_length(gcode_lines):
    total_extrusion_length = 0.0
    for line in gcode_lines:
        if line.command == ('G', 1) and 'E' in line.params:
            e_value = line.params['E']
            total_extrusion_length += abs(e_value)  # Use abs to include both extrusion and retraction
    return total_extrusion_length


def calculate_filament_weight(filament_length_mm, filament_diameter_mm, filament_density_g_per_cm3):
    # Calculate the cross-sectional area of the filament in square millimeters
    filament_radius_mm = filament_diameter_mm / 2
    cross_sectional_area_mm2 = math.pi * (filament_radius_mm ** 2)
