from ollama_api import OllamaAPI, OllamaAPIError
from prompts import PromptLibrary, format_prompt

def main():
    # Initialize API
    api = OllamaAPI(model='llama3.2')
    
    # Example 1: Simple chat with code assistant
    print("\n=== Code Assistant Example ===")
    code_template = PromptLibrary.code_assistant()
    prompt_data = format_prompt(code_template, "Write a Python function to sort a list using quicksort")
    
    try:
        response = api.chat(
            prompt=prompt_data["prompt"],
            system_prompt=prompt_data["system_prompt"],
            **prompt_data["parameters"]
        )
        print("\nResponse:", response)
    except OllamaAPIError as e:
        print(f"Error: {e}")
    
    # Example 2: Technical documentation with streaming
    print("\n=== Technical Writer Example (Streaming) ===")
    tech_template = PromptLibrary.technical_writer()
    prompt_data = format_prompt(tech_template, "Explain how Python's garbage collection works")
    
    try:
        print("\nResponse: ", end="", flush=True)
        for chunk in api.chat(
            prompt=prompt_data["prompt"],
            system_prompt=prompt_data["system_prompt"],
            stream=True,
            **prompt_data["parameters"]
        ):
            print(chunk, end="", flush=True)
        print("\n")
    except OllamaAPIError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main() 