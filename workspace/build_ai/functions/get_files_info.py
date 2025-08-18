import os
from google.genai import types

# Schema
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

# Implementation
def get_files_info(working_directory, directory=""):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        abs_target_dir = os.path.abspath(os.path.join(working_directory, directory))

        # Ensure inside working dir
        if not abs_target_dir.startswith(abs_working_dir + os.sep) and abs_target_dir != abs_working_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_target_dir):
            return f'Error: Directory not found: "{directory}"'

        files = []
        for entry in os.listdir(abs_target_dir):
            entry_path = os.path.join(abs_target_dir, entry)
            size = os.path.getsize(entry_path) if os.path.isfile(entry_path) else 0
            files.append({"name": entry, "size": size})

        return files

    except Exception as e:
        return f"Error: {str(e)}"
