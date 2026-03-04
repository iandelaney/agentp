import os
import subprocess


def run_python_file(working_directory, file_path, args=None):
    """Execute a Python file within a permitted working directory.

    Args:
        working_directory (str): The permitted working directory.
        file_path (str): Path to the Python file (absolute or relative).
        args (list[str] | None): Optional arguments to pass to the script.

    Returns:
        str: Output and/or error information.
    """
    try:
        abs_working_directory = os.path.realpath(os.path.abspath(working_directory))

        # Resolve file_path against working_directory if it's relative.
        if os.path.isabs(file_path):
            absolute_file_path = os.path.realpath(os.path.abspath(file_path))
        else:
            absolute_file_path = os.path.realpath(
                os.path.abspath(os.path.join(abs_working_directory, file_path))
            )

        # Ensure the target is inside the permitted working directory.
        try:
            if os.path.commonpath([abs_working_directory, absolute_file_path]) != abs_working_directory:
                return (
                    f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
                )
        except ValueError:
            # Different drives / invalid paths can cause commonpath to raise.
            return (
                f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
            )

        # Must exist and be a regular file.
        if not os.path.isfile(absolute_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        # Must be a .py file.
        if not absolute_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", absolute_file_path]
        if args:
            command.extend([str(a) for a in args])

        completed = subprocess.run(
            command,
            cwd=abs_working_directory,
            capture_output=True,
            text=True,
            timeout=30,
        )

        stdout = (completed.stdout or "").rstrip()
        stderr = (completed.stderr or "").rstrip()

        output_lines = []
        if completed.returncode != 0:
            output_lines.append(f"Process exited with code {completed.returncode}")

        if not stdout and not stderr:
            output_lines.append("No output produced")
        else:
            if stdout:
                output_lines.append(f"STDOUT:\n{stdout}")
            if stderr:
                output_lines.append(f"STDERR:\n{stderr}")

        return "\n".join(output_lines)
    except Exception as e:
        return f"Error: executing Python file: {e}"