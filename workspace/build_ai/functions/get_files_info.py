import os

def get_files_info(working_directory, directory="."):
    try:
        # Build the full path
        full_path = os.path.join(working_directory, directory)

        # Resolve absolute paths
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Security check: ensure path stays within working_directory
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        # Ensure it's a directory
        if not os.path.isdir(abs_full_path):
            return f'Error: "{directory}" is not a directory'

        # List directory contents
        items = os.listdir(abs_full_path)
        lines = []
        for item in items:
            item_path = os.path.join(abs_full_path, item)
            is_dir = os.path.isdir(item_path)
            try:
                size = os.path.getsize(item_path)
            except OSError as e:
                return f"Error: Unable to get size for '{item}': {e}"

            lines.append(f"- {item}: file_size={size} bytes, is_dir={is_dir}")

        # Build final output
        if directory == ".":
            header = "Result for current directory:"
        else:
            header = f"Result for '{directory}' directory:"
        return "\n".join([header] + lines)

    except Exception as e:
        return f"Error: {str(e)}"
