import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
	if(len(sys.argv) < 2):
		print("Usage: uv run main.py <input>")
		exit(1)
	input_string = sys.argv[1]
	load_dotenv()
	api_key = os.environ.get("GEMINI_API_KEY")
	client = genai.Client(api_key=api_key)

	messages = [
		types.Content(role="user", parts=[types.Part(text=input_string)]),
	]

	response = client.models.generate_content(model="gemini-2.0-flash-001", contents=messages)
	print(response.text)
	if ("--verbose" in sys.argv[2:]):
		print(f"User prompt: {input_string}")
		print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
		print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


if __name__ == "__main__":
    main()
