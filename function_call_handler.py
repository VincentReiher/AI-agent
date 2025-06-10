from google import genai

from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

WORKING_DIR = "./calculator"
FUNCTION_DICT = {
    "get_files_info" : get_files_info,
    "get_file_content" : get_file_content,
    "write_file" : write_file,
    "run_python_file" : run_python_file,
}

def call_function(function_call, verbose=False):
    if verbose: print(f"Calling function: {function_call.name}({function_call.args})")
    else: print(f" - Calling function: {function_call.name}")

    if function_call.name not in FUNCTION_DICT:
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unknown function: {function_call.name}"},
                )
            ],
        )
    function_args = function_call.args
    function_args['working_directory'] = WORKING_DIR
    try:
        function_result = FUNCTION_DICT[function_call.name](**function_args)
    except TypeError:
        print(function_args)
        return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_call.name,
                    response={"error": f"Unexpected keyword argument"},
                )
            ],
        )

    return genai.types.Content(
            role="tool",
            parts=[
                genai.types.Part.from_function_response(
                    name=function_call.name,
                    response={"result": function_result},
                )
            ]
        )