import os, argparse, json
from prompts import *
from call_function import *
from dotenv import load_dotenv
from openai import OpenAI

def main():
    try:
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

        full_response = client.chat.completions.create(model="openrouter/free", messages=messages, tools=available_functions, temperature=0) # type: ignore

        if full_response.usage == None:
            raise RuntimeError("API request failed")

        prompt_tokens = full_response.usage.prompt_tokens
        response_tokens = full_response.usage.completion_tokens

        message = full_response.choices[0].message

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {prompt_tokens}")
            print(f"Response tokens: {response_tokens}")

        if not message.tool_calls and message.content:
            print(f"Response:\n{message.content}")

        if message.tool_calls:
            for tool_call in message.tool_calls:
                if tool_call.type != "function":
                    continue
                result_message = call_function(tool_call, args.verbose)

                if not result_message.get("content"):
                    raise Exception("Error: message has no content")

                if args.verbose:
                    print(f"-> {result_message['content']}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
