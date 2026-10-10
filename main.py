import os, argparse, sys
from prompts import *
from call_function import *
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
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
    ]

def generate_chat():
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions, # type: ignore
        )

    if response.usage is None:
        raise RuntimeError("API request failed")

    prompt_tokens = response.usage.prompt_tokens
    response_tokens = response.usage.completion_tokens

    chat_output = response.choices[0].message
    messages.append(chat_output)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Response tokens: {response_tokens}")

    if not chat_output.tool_calls:
         print(f"Response:\n{chat_output.content}")
         return True

    for tool_call in chat_output.tool_calls:
        if tool_call.type != "function":
              continue
    
        call_output = call_function(tool_call, args.verbose)
        messages.append(call_output)

        if not call_output.get("content"):
             raise RuntimeError(f"Empty function response for {tool_call.function.name}")

        if args.verbose:
            print(f"-> {call_output["content"]}")

    return False


def main():
    for _ in range(20):
        task = generate_chat()

        if task:
            break
    else:
        print("Maximum number of iterations reached. Task not completed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
