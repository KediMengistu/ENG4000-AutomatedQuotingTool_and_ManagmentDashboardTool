import re

def parse_gcode_file(file_path):
    # A dict to hold the parsed data
    parsed_data = {
        'comments': [],
        'commands': []
    }

    # Regular expression to match comments and GCode commands
    comment_re = re.compile(r';(.*)')
    command_re = re.compile(r'([GM]\d+)\s+(.*)')

    try:
        with open(file_path, 'r') as file:
            for line in file:
                # Strip leading and trailing whitespace
                stripped_line = line.strip()

                # Check for comments
                comment_match = comment_re.match(stripped_line)
                if comment_match:
                    # Add the comment text to the dict
                    parsed_data['comments'].append(comment_match.group(1).strip())

                # Check for GCode commands
                command_match = command_re.match(stripped_line)
                if command_match:
                    # Add the command and its arguments to the dict
                    parsed_data['commands'].append({
                        'command': command_match.group(1),
                        'args': command_match.group(2).strip()
                    })

    except IOError as e:
        print(f"Error opening file {file_path}: {e}")

    return parsed_data


# # Replace 'path_to_your_gcode_file.gcode' with the actual file path
# gcode_file_path = 'path_to_your_gcode_file.gcode'
# parsed_gcode = parse_gcode_file(gcode_file_path)
#
# # Output the parsed comments and commands
# print(parsed_gcode['comments'])
# print(parsed_gcode['commands'])