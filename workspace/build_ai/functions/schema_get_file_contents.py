schema_get_file_content = {
    "name": "get_file_content",
    "description": "Read the contents of a file",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "The path of the file to read"
            }
        },
        "required": ["file_path"]
    },
}

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

schema_write_file = {
    "name": "write_file",
    "description": "Write or overwrite a file with given content",
    "parameters": {
        "type": "object",
        "properties": {
            "file_path": {
                "type": "string",
                "description": "Path to the file to write to"
            },
            "content": {
                "type": "string",
                "description": "The content to write into the file"
            }
        },
        "required": ["file_path", "content"]
    },
}
