def main():
    import os
    import sys
    import argparse

    from dotenv import load_dotenv
    from google import genai
    from google.genai import types

    from prompts import system_prompt
    from call_functions import available_functions, call_function

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="add a Prompt in quotes")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise ValueError("GEMINI_API_KEY not found in environment variables.")

    client = genai.Client(api_key=api_key)

    # Conversation history (must persist across iterations)
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)]),
    ]

    for _ in range(20):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
            ),
        )

        # Add ALL candidates to history early in the loop
        if not response.candidates:
            raise RuntimeError("Gemini API response has no candidates")

        for cand in response.candidates:
            if cand.content is not None:
                messages.append(cand.content)

        # Handle function calls (if any)
        function_calls = getattr(response, "function_calls", None)
        if function_calls:
            function_responses = []

            for fc in function_calls:
                function_call_result = call_function(fc, verbose=args.verbose)

                # parts must be non-empty
                if not function_call_result.parts:
                    raise RuntimeError("Tool call returned Content with empty .parts")

                # function_response must exist
                fr = function_call_result.parts[0].function_response
                if fr is None:
                    raise RuntimeError("Tool call returned Part with function_response=None")

                # response must exist
                if fr.response is None:
                    raise RuntimeError("Tool call returned FunctionResponse with response=None")

                # Store the Part for later
                function_responses.append(function_call_result.parts[0])

                # Verbose print (exact format required)
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            # Append tool results back into conversation history
            messages.append(types.Content(role="user", parts=function_responses))

            # Continue loop so the model can use tool outputs
            continue

        # No function calls => final response
        print("Final response:")
        print(response.text)
        return

    # If we get here, we hit max iterations without a final response
    print("Error: reached maximum iterations (20) without producing a final response.")
    sys.exit(1)


if __name__ == "__main__":
    main()