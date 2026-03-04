import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

def get_files_info(working_directory, directory="."):
    try:
        # 1. Get the real, full path of our 'safe' zone
        working_dir_abs = os.path.abspath(working_directory)
        
        # 2. Combine it with the requested folder and clean it up
        # This handles things like "folder/../other_folder"
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        # 3. Now we check: is the common path still our safe zone?
        if os.path.commonpath([working_dir_abs, target_dir]) != working_dir_abs:
            # Return the error string if they tried to escape!
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        # Right after the security check:
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        files_info = []
        # Loop over names in the target directory
        for name in os.listdir(target_dir):
            # Get the full path for this specific item
            filepath = os.path.join(target_dir, name)
            
            # Get the information we need
            is_dir = os.path.isdir(filepath)
            size = os.path.getsize(filepath)
            
            # Format the string exactly as the lesson asks
            info_str = f"- {name}: file_size={size} bytes, is_dir={is_dir}"
            files_info.append(info_str)

        # Finally, join the list into one big string with newlines
        return "\n".join(files_info)
    except Exception as e:
    # If an error happens, return a string that starts with "Error:"
        return f"Error: {e}"