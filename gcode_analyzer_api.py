# import os
# import requests
#
# API_ENDPOINT = "https://gcode.ws/"
#
# def analyze_gcode_file(gcode_file_path):
#     if os.path.exists(gcode_file_path):
#         with open(gcode_file_path, "rb") as gcode_file:
#             files = {"file": ("file.gcode", gcode_file)}
#             response = requests.post(API_ENDPOINT, files=files)
#
#         if response.status_code == 200:
#             return response.text  # Return the API response content
#         else:
#             return f"Error: {response.status_code}"
#     else:
#         return "Error: File not found"