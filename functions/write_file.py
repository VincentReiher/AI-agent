import os

def write_file(working_directory, file_path, content):
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: cannot write "{file_path}" as it is outside the permitted working directory'
    
    file_dest_data = abs_file_path.rsplit("/", maxsplit=1)
    os.makedirs(file_dest_data[0], exist_ok = True)

    try:
        with open(abs_file_path, "w") as f:
            f.write(content)
    except:
        return f'Error: unknown error occurred'
    
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    