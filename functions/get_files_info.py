import os

MAXIMUM_FILE_LENGTH = 10000

def get_files_info(working_directory, directory=None):
    abs_working_dir = os.path.abspath(working_directory)

    src_dir = os.path.join(working_directory, directory)
    abs_src_dir = os.path.abspath(src_dir)

    if not abs_src_dir.startswith(abs_working_dir):
        return f'Error: cannot list \"{directory}\" as it is outside the permitted working directory'
    
    if not os.path.isdir(abs_src_dir):
        return f'Error: \"{directory}\" is not a directory'
    
    return_str = []
    try:
        for element in os.listdir(abs_src_dir):
            element_path = os.path.join(abs_src_dir, element)
            is_dir = os.path.isdir(element_path)
            file_size = os.path.getsize(element_path)

            return_str.append(f'{element}: file_size={file_size} bytes, is_dir={is_dir}')
    except FileNotFoundError:
        return f'Error: \"{directory}\" does not exist'

    return "\n".join(return_str)

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