import os
from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python_file import run_python_file

def call_function(call, verbose=False):
	if(verbose):
		print(f"Calling function: {call.name}({call.args})")
	else:
		print(f" - Calling function: {call.name}")
	k_args = call.args.copy()
	k_args['working_directory'] = 'calculator'
	functions_dict = {}
	functions_dict['get_files_info'] = get_files_info
	functions_dict['get_file_content'] = get_file_content
	functions_dict['write_file'] = write_file
	functions_dict['run_python_file'] = run_python_file
	if(call.name not in functions_dict):
		return types.Content(
			role="tool",
			parts=[
				types.Part.from_function_response(
					name=call.name,
					response={"Error": f"Unknown function: {call.name}"},
				)
			],
		)
	else:
		function_result = functions_dict[call.name](**k_args)
	return types.Content(
		role="tool",
		parts=[
			types.Part.from_function_response(
				name=call.name,
				response={"result": function_result},
			)
		],
	)



