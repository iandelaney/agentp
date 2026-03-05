from google.genai import types

# --- import schemas (declarations) ---
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.get_file_content import schema_get_file_content, get_file_content
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_file import schema_write_file, write_file


# 1) Tool registry for Gemini
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_run_python_file,
        schema_write_file,
    ],
)


# 2) Dispatcher/executor for tool calls
def call_function(function_call, verbose: bool = False):
    """
    Execute a Gemini tool call safely by mapping function name -> real function,
    injecting working_directory, and returning a types.Content tool response.
    """

    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "run_python_file": run_python_file,
        "write_file": write_file,
    }

    function_name = function_call.name or ""

    if verbose:
        print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f" - Calling function: {function_call.name}")

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )

    # Copy args (or empty dict if None)
    args = dict(function_call.args) if function_call.args else {}

    # Inject working directory (do NOT let the model control this)
    args["working_directory"] = "./calculator"

    # Execute the underlying function
    function_result = function_map[function_name](**args)

    # Wrap result in tool response content
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )