schema_get_files_info = {
    "name": "get_files_info",
    "description": "Get a list of files and directories inside a given directory",
    "parameters": {
        "type": "object",
        "properties": {
            "directory": {
                "type": "string",
                "description": "The directory path to list"
            }
        },
        "required": ["directory"]
    },
}
