import os, subprocess

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_work_dir, file_path))
        valid_target_dir = os.path.commonpath([abs_work_dir, target_file]) == abs_work_dir

        if not valid_target_dir:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        elif not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        elif not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]

        if args != None:
            command.extend(args)

        output = subprocess.run(command, cwd=abs_work_dir, capture_output=True, timeout=30, text=True)

        output_parts = []

        if output.returncode != 0:
            output_parts.append(f'Process exited with code {output.returncode}')
        elif output.stdout == None and output.stderr == None:
            output_parts.append("No output produced")
        else:
            output_parts.append(f'STDOUT: {output.stdout}')
            output_parts.append(f'STDERR: {output.stderr}')

        return "\n".join(output_parts)
    except Exception as e:
        return f"Error: executing Python file: {e}"