import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# ----------------------------
# Function schema & tool setup
# ----------------------------
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)

available_functions = types.Tool(
    function_declarations=[schema_get_files_info]
)

# ----------------------------
# Local function implementation
# ----------------------------
def get_files_info(directory="."):
    """Lists files in a directory (relative to working directory) with security checks."""
    working_directory = os.getcwd()  # Hardcoded to current working directory
    try:
        # Build the full path
        full_path = os.path.join(working_directory, directory)

        # Resolve absolute paths
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Security check
        if not abs_full_path.startswith(abs_working_directory):
            return {"error": f'Cannot list "{directory}" as it is outside the permitted working directory'}

        # Ensure it's a directory
        if not os.path.isdir(abs_full_path):
            return {"error": f'"{directory}" is not a directory'}

        # Collect directory contents
        items_info = []
        for item in os.listdir(abs_full_path):
            item_path = os.path.join(abs_full_path, item)
            try:
                size = os.path.getsize(item_path)
            except OSError:
                size = None  # If we can't get size, set None

            items_info.append({
                "name": item,
                "file_size": size,
                "is_dir": os.path.isdir(item_path)
            })

        return {
            "directory": directory,
            "items": items_info
        }

    except Exception as e:
        return {"error": str(e)}

# ----------------------------
# System prompt
# ----------------------------
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# ----------------------------
# Main CLI logic
# ----------------------------
if len(sys.argv) < 2:
    print("Usage: python main.py '<your prompt here>' [--verbose]")
    sys.exit(1)

user_input = sys.argv[1]
verbose = "--verbose" in sys.argv

# Load API key and init client
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Call the model
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=user_input,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
)

# Check if function was called
if hasattr(response, "function_calls") and response.function_calls:
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")

        # Actually run the function locally
        if function_call_part.name == "get_files_info":
            directory_arg = function_call_part.args.get("directory", ".")
            result = get_files_info(directory_arg)
            print(result)
else:
    print(response.text)

#
