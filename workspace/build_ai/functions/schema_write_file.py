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