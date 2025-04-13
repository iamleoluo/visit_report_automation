from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class PromptTemplate:
    system: str
    user: str
    parameters: Dict[str, Any]

class PromptLibrary:
    @staticmethod
    def general_assistant() -> PromptTemplate:
        return PromptTemplate(
            system="You are a helpful, concise, and friendly AI assistant.",
            user="{user_input}",
            parameters={
                "temperature": 0.7,
                "top_p": 0.9
            }
        )
    
    @staticmethod
    def code_assistant() -> PromptTemplate:
        return PromptTemplate(
            system="""You are an expert programming assistant. Focus on:
- Writing clean, efficient code
- Following best practices and design patterns
- Providing clear explanations
- Including necessary error handling
- Writing comprehensive documentation""",
            user="{user_input}",
            parameters={
                "temperature": 0.2,
                "top_p": 0.9
            }
        )
    
    @staticmethod
    def technical_writer() -> PromptTemplate:
        return PromptTemplate(
            system="""You are a technical documentation expert. Focus on:
- Clear and concise explanations
- Proper formatting and structure
- Technical accuracy
- Examples and use cases
- Best practices and guidelines""",
            user="{user_input}",
            parameters={
                "temperature": 0.4,
                "top_p": 0.9
            }
        )

def format_prompt(template: PromptTemplate, user_input: str, **kwargs) -> Dict[str, Any]:
    """Format a prompt template with user input and additional parameters.
    
    Args:
        template: PromptTemplate to use
        user_input: User's input text
        **kwargs: Additional formatting parameters
        
    Returns:
        Dict containing formatted prompt and parameters
    """
    return {
        "system_prompt": template.system,
        "prompt": template.user.format(user_input=user_input, **kwargs),
        "parameters": template.parameters
    }

# Example usage:
"""
from ollama_api import OllamaAPI
from prompts import PromptLibrary, format_prompt

# Initialize API
api = OllamaAPI()

# Use code assistant template
code_template = PromptLibrary.code_assistant()
prompt_data = format_prompt(code_template, "Write a Python function to calculate fibonacci numbers")

# Get response
response = api.chat(
    prompt=prompt_data["prompt"],
    system_prompt=prompt_data["system_prompt"],
    **prompt_data["parameters"]
)
""" 