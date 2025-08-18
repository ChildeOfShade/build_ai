import os
import subprocess

# Schema for the LLM
schema_run_python_file = {
    "name": "run_python_file",
    "description": "Execute a Python file with optional arguments",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the Python file to run"
            },
            "args": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Optional arguments to pass to the Python file"
            }
        },
        "required": ["file_path"]
    },
}

# Function to actually run the Python file
def run_python_file(working_directory, file_path, args=None):
    args = args or []
    full_path = os.path.join(working_directory, file_path)

    if not os.path.isfile(full_path):
        return f'Error: File "{full_path}" not found'

    cmd = ["python3", full_path] + args
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"result": result.stdout.strip()}
    except subprocess.CalledProcessError as e:
        return {"result": f"Error: {e.stderr.strip()}"}
