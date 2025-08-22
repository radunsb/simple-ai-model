import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
	name="get_files_info",
	description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"directory": types.Schema(
				type=types.Type.STRING,
				description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
			)
		},
	),
)

def get_files_info(working_directory, directory="."):
	try:
		unnormalized_path = os.path.join(working_directory, directory)
	except Exception as e:
		return f"Error: {e}"
	try:
		full_path = os.path.normpath(unnormalized_path)
	except Exception as e:
		return f"Error: {e}"
	if not full_path.startswith(working_directory):
		return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
	try:
		if not os.path.isdir(full_path):
			return f"Error: \"{directory}\" is not a directory"
	except Exception as e:
		return f"Error: {e}"
	try:
		children = os.listdir(full_path)
	except Exception as e:
		return f"Error: {e}"
	to_return = ""
	for child in children:
		child_path = full_path + "/" + child
		to_return += f"- {child}: file_size={os.path.getsize(child_path)} bytes, is_dir={os.path.isdir(child_path)}\n"
	return to_return
