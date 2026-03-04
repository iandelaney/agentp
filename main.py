def main():
    import os
    import argparse

    from dotenv import load_dotenv
    from google import genai
    from google.genai import types

    from prompts import system_prompt
    from call_functions import available_functions

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="add a Prompt in quotes")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt,
        ),
    )

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    # Assignment requirement: print function calls if any, otherwise print text
    function_calls = getattr(response, "function_calls", None)
    if function_calls:
        for function_call in function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print("Response:")
        print(response.text)

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)


if __name__ == "__main__":
    main()