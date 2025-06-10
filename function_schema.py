from google import genai

schema_get_files_info = genai.types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "directory": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

schema_get_file_content = genai.types.FunctionDeclaration(
    name="get_file_content",
    description="Returns the contents of a file as a string up to a maximum character length, constrained to the working directory.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The text file to be read, relative to the working directory.",
            ),
        },
    ),
)

schema_write_file = genai.types.FunctionDeclaration(
    name="write_file",
    description="Writes the contents of a string to a file within the working directory. Safely creates any missing subfolders.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The text file to be written, relative to the working directory.",
            ),
            "content": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The contents of the new file to be written."
            )
        },
    ),
)

schema_run_python_file = genai.types.FunctionDeclaration(
    name="run_python_file",
    description="Executes the python code from a file within the working directory. Returns all STDOUT and STDERR messages.",
    parameters=genai.types.Schema(
        type=genai.types.Type.OBJECT,
        properties={
            "file_path": genai.types.Schema(
                type=genai.types.Type.STRING,
                description="The python file to be executed, relative to the working directory.",
            )
        },
    ),
)

available_functions = genai.types.Tool(
                                    function_declarations= [
                                        schema_get_files_info,
                                        schema_get_file_content,
                                        schema_write_file,
                                        schema_run_python_file
                                    ]
                                )