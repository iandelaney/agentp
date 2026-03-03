def write_file(working_directory, file_path, content):
    import os
    try:
        # 1. Get the real, full path of our 'safe' zone
        working_dir_abs = os.path.abspath(working_directory)
        
        # 2. Combine it with the requested file path and clean it up
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # 3. Now we check: is the common path still our safe zone?
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            # Return the error string if they tried to escape!
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        # Ensure the directory exists before writing
        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        # Write the content to the file
        with open(target_file, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        # If an error happens, return a string that starts with "Error:"
        return f"Error: {e}"