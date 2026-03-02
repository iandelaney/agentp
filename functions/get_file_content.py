def get_file_content(working_directory, file_path):
    import os
    from config import MAX_CHARS

    try:
        # 1. Get the real, full path of our 'safe' zone
        working_dir_abs = os.path.abspath(working_directory)
        
        # 2. Combine it with the requested file and clean it up
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        # 3. Now we check: is the common path still our safe zone?
        if os.path.commonpath([working_dir_abs, target_file]) != working_dir_abs:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        
        with open(target_file, 'r') as f:
            content = f.read(MAX_CHARS)
            extra = f.read(1)
            if extra:
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        
        
        return content
    except Exception as e:
        return f"Error: {e}"