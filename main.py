import os, argparse
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
api_key = os.environ.get("OPENROUTER_API_KEY")
if api_key is None:
    raise RuntimeError("No API key found")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser(description="Chatbot")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()

messages = [
    {
        "role": "user",
        "content": args.user_prompt,
    }
]

full_response = client.chat.completions.create(model="openrouter/free", messages=messages) # type: ignore

response_content = full_response.choices[0].message.content

if full_response.usage == None:
    raise RuntimeError("API request failed")

prompt_tokens = full_response.usage.prompt_tokens
response_tokens = full_response.usage.completion_tokens

def print_messages():
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")
        print(response_content)
    else:
        print(response_content)

def main():
    print_messages()


if __name__ == "__main__":
    main()
