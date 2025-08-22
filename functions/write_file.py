import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
	name="write_file",
	description="Overwrites a file with the specified content. Constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The path of the file to write to, relative to the working directory.",
			),
			"content": types.Schema(
				type=types.Type.STRING,
				description="The text content which will be written to the file.",
			),
		},
	),
)


def write_file(working_directory, file_path, content):
	full_path = os.path.normpath(os.path.join(working_directory, file_path))
	if not full_path.startswith(working_directory):
		return f"Error: Cannot write to \"{file_path}\" as it is outside the permitted working directory"
	if not os.path.exists(full_path):
		things_list = file_path.split("/")
		directory_for_file = file_path + "/".join(things_list[:-1])
		if not os.path.exists(directory_for_file):
			os.makedirs(directory_for_file)		
	try:
		with open(full_path, "w") as f:
			f.write(content)
			return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
	except Exception as e:
		return f"Error: {e}"
