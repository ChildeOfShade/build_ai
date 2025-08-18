import os
import sys
import unittest
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Import schemas and implementations
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import schema_write_file, write_file

# ------------------------------
# Step 1: Create a Tool with all schemas
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
    ]
)

# ------------------------------
# Step 2: Create the system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. 
You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. 
You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# ------------------------------
# Step 3: Check for CLI args
if len(sys.argv) < 2:
    print("Usage: python main.py '<your prompt here>' [--verbose]")
    sys.exit(1)

user_input = sys.argv[1]
verbose = "--verbose" in sys.argv

# ------------------------------
# Special case: run tests.py directly
if user_input.strip() == "run tests.py":
    # Discover and run all tests in the current directory
    loader = unittest.TestLoader()
    suite = loader.discover(".")
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    # Exit with code 0 if all tests pass, 1 otherwise
    sys.exit(0 if result.wasSuccessful() else 1)

# ------------------------------
# Step 4: Load API key & initialize client
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# ------------------------------
# Step 5: Define dispatcher for function calls
def call_function(function_call_part, verbose=False):
    name = function_call_part.name
    args = dict(function_call_part.args)

    # Only inject working_directory if not already provided
    if "working_directory" not in args:
        args["working_directory"] = "./calculator"  # default for normal files

    # But if the file is in root, override for tests.py
    if args.get("file_path") == "tests.py":
        args["working_directory"] = "."  # run from root

    if verbose:
        print(f"[Dispatcher] Calling function: {name}({args})")
    else:
        print(f" - Calling function: {name}")

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    if name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=name,
                    response={"error": f"Unknown function: {name}"},
                )
            ],
        )

    # Call the actual function
    result = function_map[name](**args)

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=name,
                response={"result": result},
            )
        ],
    )

# ------------------------------
# Step 6: Call the model
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=user_input,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
)

# ------------------------------
# Step 7: Handle function calls
if hasattr(response, "function_calls") and response.function_calls:
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose=verbose)

        if not function_call_result.parts or not function_call_result.parts[0].function_response.response:
            raise RuntimeError("Function call failed: No response returned")

        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
else:
    print(response.text)

# ------------------------------
# Step 8: Verbose mode output
if verbose:
    print(f"User prompt: {user_input}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
