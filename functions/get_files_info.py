import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_work_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_work_dir, directory))
        valid_target_dir = os.path.commonpath([abs_work_dir, target_dir]) == abs_work_dir

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        elif not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        dir_contents = os.listdir(target_dir)
        info_list = []

        for item in dir_contents:
            name = os.path.join(target_dir, item)
            file_size = os.path.getsize(name)
            is_dir = os.path.isdir(name)
            item_info = f"- {item}: file_size={file_size}, is_dir={is_dir}"
            info_list.append(item_info)

        info_string = "\n".join(info_list)

        return info_string
    except Exception as e:
        return f"Error: {e}"

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": "directory",
        },
    },
}