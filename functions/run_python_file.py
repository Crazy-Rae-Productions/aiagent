import os, subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))
        valid_target_file = os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args != None:
            command.extend(args)

        output = subprocess.run(command, cwd=abs_work_dir, capture_output=True, timeout=30, text=True)

        output_parts = []

        if output.returncode != 0:
            output_parts.append(f'Process exited with code {output.returncode}')
        
        if output.stdout is None and output.stderr is None:
            output_parts.append("No output produced")
        else:
            output_parts.append(f'STDOUT: {output.stdout}')
            output_parts.append(f'STDERR: {output.stderr}')

        return "\n".join(output_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs a Python file with optional arguments within the working directory, returning the appropriate standard output or error messages",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "A Python file to execute within the working directory",
                },
                "args": {
                    "type": "array",
                    "description": "A list of additional commands to run within the subprocess (may also be empty)",
                    "items": {
                        "type": "string",
                    },
                },
            },
            "required": ["file_path"],
        },
    },
}