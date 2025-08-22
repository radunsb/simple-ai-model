import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
	try:
		full_path = os.path.normpath(os.path.join(working_directory, file_path))
		if not full_path.startswith(working_directory):
			return f"Error: Cannot execute \"{file_path}\" as it is outside the permitted working directory"
		if not os.path.exists(full_path):
			return f"Error: File \"{file_path}\" not found."
		if not full_path.endswith(".py"):
			return f"Error: \"{file_path}\" is not a Python file."
		if len(args) >= 1:
			args.insert(0, file_path)
			args.insert(0, "python")
			to_run = args.copy()
		else:
			to_run = ["python", file_path]
		completed_process = subprocess.run(to_run, cwd=working_directory, timeout=30, capture_output=True)
		output_string = f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"
		if completed_process.returncode != 0:
			output_string += " Process exited with code X"
		if completed_process.stdout == None:
			return "No output prouced"
		else:
			return output_string
	except Exception as e:
		return f"Error: executing Python file: {e}"
