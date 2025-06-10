import os, sys
from dotenv import load_dotenv

from google import genai

from function_call_handler import call_function

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read the contents of a text file
- Write text to a file
- Execute python code

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

model_name = 'gemini-2.0-flash-001'

MAXIMUM_LLM_CALLS = 20

def main():
    # Load API key from file
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    verbose = False

    # Gather user prompt from CLI
    if len(sys.argv) < 2:
        print("Missing prompt")
        exit(1)
    if len(sys.argv) > 2:
        for arg in sys.argv[2:]:
            if arg == "--verbose":
                verbose = True
    user_prompt = sys.argv[1]
    if verbose: 
        print(f"User prompt: {user_prompt}")
    messages = [
        genai.types.Content(role="user", parts=[genai.types.Part(text=user_prompt)]),
    ]

    # LLM-available function calls
    from function_schema import available_functions

    # Configure LLM
    LLM_config = genai.types.GenerateContentConfig(
        system_instruction=system_prompt,
        tools=[available_functions]
    )
    LLM_call = 0
    while(LLM_call < MAXIMUM_LLM_CALLS):

        # Call LLM with user prompt
        response = client.models.generate_content(model=model_name, 
                                                contents=messages,
                                                config=LLM_config)
        
        if response.candidates != []:
            for candidate in response.candidates:
                messages.append(candidate.content)

        if response.function_calls is not None:
            for function_call in response.function_calls:
                function_return = call_function(function_call, verbose=verbose)
                
                try:
                    print_message = f"-> {function_return.parts[0].function_response.response}"
                except AttributeError:
                    raise Exception("FATAL: An unknown error occurred.")
                
                if verbose:
                    print(print_message)

                messages.append(function_return)
                
        if response.function_calls is not None:
            LLM_call += 1
            continue
        else:
            print(response.text)
            break
        
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()