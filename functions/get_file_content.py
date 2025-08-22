import os
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
	name="get_file_content",
	description="Reads the content of a specified file, truncated at 10000 characters. Constrained to the working directory.",
	parameters=types.Schema(
		type=types.Type.OBJECT,
		properties={
			"file_path": types.Schema(
				type=types.Type.STRING,
				description="The path of the file to read from, relative to the working directory.",
			)
		},
	),
)


def get_file_content(working_directory, file_path):
	full_path = os.path.normpath(os.path.join(working_directory, file_path))
	if not full_path.startswith(working_directory):
		return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
	if not os.path.isfile(full_path):
		return f"Error: File not found or is not a regular file: \"{file_path}\""
	try:
		with open(full_path) as f:
			content = f.read()
			if(len(content) > 10000):
				content = content[:10000] + f"[...File \"{file_path}\" truncated at 10000 character]"
			return content
	except Exception as e:
		return f"Error: {e}"
		

