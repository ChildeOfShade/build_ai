import os
from google.genai import types
from functions.config import MAX_FILE_CHARS

# Function schema (for Gemini)
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read the contents of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)

# Function implementation (what actually runs)
def get_file_content(working_directory, file_path):
    try:
        # Resolve the absolute paths
        abs_working_dir = os.path.abspath(working_directory)
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))

        # Ensure file is inside working directory
        if not abs_file_path.startswith(abs_working_dir + os.sep):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Ensure it's a regular file
        if not os.path.isfile(abs_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        # Read file contents
        with open(abs_file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Truncate if necessary
        if len(content) > MAX_FILE_CHARS:
            content = content[:MAX_FILE_CHARS] + f'[...File "{file_path}" truncated at {MAX_FILE_CHARS} characters]'

        return content

    except Exception as e:
        return f"Error: {str(e)}"
