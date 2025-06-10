import os
import subprocess

def run_python_file(working_directory, file_path):

    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    abs_working_directory = os.path.abspath(working_directory)

    if not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    file_name, file_ext = file_path.rsplit(".", maxsplit=1)

    if file_ext != "py":
        return f'Error: File \"{file_path}\" is not a Python file.'
    try:
        with open(abs_file_path) as f:
            pass
    except FileNotFoundError:
        return f'Error: File \"{file_path}\" not found.'
    
    try:
        file_return = subprocess.run(["python3", abs_file_path],
                                     encoding='utf-8', 
                                     stdout=subprocess.PIPE, 
                                     timeout=30)
    except Exception as e:
        return f'Error: executing Python file: {e}'
    
    return_str = []

    if file_return.stdout != "":
        return_str.append("STDOUT: " + file_return.stdout)

    if file_return.stderr is not None:
        return_str.append("STDERR: " + file_return.stderr)

    if file_return.stdout == "" and file_return.stderr == "":
        return_str.append("No output produced.")

    if file_return.returncode:
        return_str.append(f'Process exited with code {file_return.returncode}')
    
    return "\n".join(return_str)