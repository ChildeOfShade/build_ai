from google.genai import types

schema_run_python_file = types.FunctionSchema(
    name="run_python_file",
    description="Execute a Python file with optional arguments",
    parameters=[
        types.FunctionParameter(
            name="file_path",
            type=str,
            description="Path to the Python file to run",
            required=True,
        ),
        types.FunctionParameter(
            name="args",
            type=list,
            description="Optional arguments to pass to the Python file",
            required=False,
        ),
    ]
)
