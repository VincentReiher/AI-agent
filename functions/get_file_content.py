import os

MAXIMUM_FILE_LENGTH = 10000

def get_file_content(working_directory, file_path):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        with open(abs_file_path, "r") as f:
            contents = f.read()
    except FileNotFoundError:
        return f'Error: File not found or is not a regular file: \"{file_path}\"'
    
    if len(contents) > MAXIMUM_FILE_LENGTH:
        contents = contents[:MAXIMUM_FILE_LENGTH]
        contents += f'\n[...File \"{file_path}\" truncated at {MAXIMUM_FILE_LENGTH} characters]'

    return contents