from functions.get_files_info import *
from functions.get_file_content import *
from functions.run_python_file import *
from functions.write_file import *

import json
from collections.abc import Callable

available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_run_python_file,
    schema_write_file,
]

def call_function(tool_call, verbose: bool = False) -> dict:
    try:
        function_name = tool_call.function.name
        function_args = json.loads(tool_call.function.arguments or "{}")
        function_args["working_directory"] = "./calculator"

        function_map: dict[str, Callable[..., str]] = {
            "get_file_content": get_file_content,
            "get_files_info": get_files_info,
            "run_python_file": run_python_file,
            "write_file": write_file,
            }
        
        result = function_map[function_name](**function_args)

        if verbose == True:
            print(f" - Calling function: {function_name}({function_args})")
        else:
            print(f" - Calling function: {function_name}")

        tool_message = {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": result,
        }

        if function_name not in function_map:
            return {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": f"Error: Unknown function: {function_name}",
            }
        else:
            return tool_message
    except Exception as e:
        print(f"Error: {e}")