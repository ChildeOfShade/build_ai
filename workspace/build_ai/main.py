import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Step 1: Define the function schema
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

# Step 2: Create a Tool with the schema
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)

# Step 3: Create the system prompt
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

# Step 4: Check for CLI args
if len(sys.argv) < 2:
    print("Usage: python main.py '<your prompt here>' [--verbose]")
    sys.exit(1)

user_input = sys.argv[1]
verbose = "--verbose" in sys.argv

# Step 5: Load API key & initialize client
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Step 6: Call the model with tools and system instructions
response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents=user_input,
    config=types.GenerateContentConfig(
        tools=[available_functions],
        system_instruction=system_prompt
    )
)

# Step 7: Check if LLM called a function
if hasattr(response, "function_calls") and response.function_calls:
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
else:
    print(response.text)

# Step 8: Verbose mode output
if verbose:
    print(f"User prompt: {user_input}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
