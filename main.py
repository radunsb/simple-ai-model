import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
	if(len(sys.argv) < 2):
		print("Usage: uv run main.py <input>")
		exit(1)
	input_string = sys.argv[1]
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	client = genai.Client(api_key=api_key)
	system_prompt = system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""
	messages = [
		types.Content(role="user", parts=[types.Part(text=input_string)]),
	]
	available_functions = types.Tool(
		function_declarations=[
			schema_get_files_info,
			schema_get_file_content,
			schema_run_python_file,
			schema_write_file
		]
	)
	
	response = client.models.generate_content(
		model="gemini-2.0-flash-001", 
		contents=messages,
		config=types.GenerateContentConfig(
			tools=[available_functions],
			system_instruction=system_prompt
		)
	)
	if(len(response.function_calls) > 0):
		for call in response.function_calls:
			content_return = call_function(call)
			try:
				to_print = content_return.parts[0].function_response.response
				if ("--verbose" in sys.argv[2:]):
					print(f"-> {content_return.parts[0].function_response.response}")
			except Exception as e:
				raise Exception("Content did not contain function response")
				
	else:
		print(response.text)
	if ("--verbose" in sys.argv[2:]):
		print(f"User prompt: {input_string}")
		print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
		print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
