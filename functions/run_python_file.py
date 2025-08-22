import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
	name="run_python_file",
	description="Runs a python file with specified arguments and prints the output. If there is an error, it will print the error message and exit code. Constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The path of the python file which will be run, relative to the working directory",
			),
			"args": types.Schema(
				type=types.Type.ARRAY,
				description="An optional list of arguments that the file will be run with.",
				items=types.Schema(
					type=types.Type.STRING,
				),
			)
		},
	),
)


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
