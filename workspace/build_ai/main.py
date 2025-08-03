import os
import sys
from dotenv import load_dotenv
from google import genai

# Check if a prompt was provided
if len(sys.argv) < 2:
    print("Usage: python main.py '<your prompt here>' [--verbose]")
    sys.exit(1)

user_input = sys.argv[1]  # First argument: the prompt
verbose = "--verbose" in sys.argv  # Check for --verbose flag

# Load environment variables
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=user_input
)

# Always print the response
print(response.text)

# Conditionally print extra info
if verbose:
    print(f"User prompt: {user_input}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
