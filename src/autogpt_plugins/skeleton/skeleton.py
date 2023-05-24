import os
import openai
import json
from typing import Dict, Any


# Command functions
def create_file(prompt: Dict[str, Any]) -> str:
    file_name = prompt["file_name"]
    initial_content = prompt.get("initial_content", "")
    with open(file_name, "w") as f:
        f.write(initial_content)
    return f"Created file {file_name}"


def write_to_file(prompt: Dict[str, Any]) -> str:
    file_name = prompt["file_name"]
    content = prompt["content"]
    with open(file_name, "a") as f:
        f.write(content)
    return f"Wrote to file {file_name}"


def create_directory(prompt: Dict[str, Any]) -> str:
    directory_name = prompt["directory_name"]
    os.makedirs(directory_name, exist_ok=True)
    return f"Created directory {directory_name}"


def change_directory(prompt: Dict[str, Any]) -> str:
    directory_name = prompt["directory_name"]
    os.chdir(directory_name)
    return f"Changed directory to {directory_name}"


def list_files(prompt: Dict[str, Any]) -> str:
    files = os.listdir()
    return "\n".join(files)


def load_code_structure():
    # If the file does not exist, return an empty dictionary
    if not os.path.isfile('code_structure.md'):
        return {}

    with open('code_structure.md', 'r') as f:
        return json.load(f)


def save_code_structure(code_structure):
    with open('code_structure.md', 'w') as f:
        json.dump(code_structure, f)


def list_code_structure(prompt: Dict[str, Any]) -> str:
    # Load the code structure from the file
    code_structure = load_code_structure()

    # Prepare a string representation
    structure = "File Descriptions:\n"
    for file, description in code_structure.items():
        structure += f"{file}: {description}\n"

    return structure


def update_code_structure(prompt: Dict[str, Any]) -> str:
    # Load the code structure from the file
    code_structure = load_code_structure()

    # Get a list of all files in the current directory
    files = [path for path in os.listdir() if os.path.isfile(path)]

    # Filter out the files that have already been described
    files = [file for file in files if file not in code_structure]

    model = os.getenv('SKELETON_MODEL', os.getenv('FAST_LLM_MODEL', 'gpt-3.5-turbo'))
    max_tokens = os.getenv('SKELETONM_TOKEN_LIMIT', os.getenv('FAST_TOKEN_LIMIT', 1500))
    temperature = os.getenv('SKELETON_TEMPERATURE', os.getenv('TEMPERATURE', 0.5))

    # Generate descriptions for the remaining files
    for file in files:
        # Call the OpenAI API for chat completion to generate a file description
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are an assistant that generates descriptions of Python code files. Please describe the following file: {file}",
                },
                {
                    "role": "user",
                    "content": open(file).read(),
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Add the generated description to the code structure
        code_structure[file] = response.choices[0].message['content']

    # Save the updated code structure to the file
    save_code_structure(code_structure)

    # Return the new file descriptions
    return "\n".join(f"{file}: {description}" for file, description in code_structure.items() if file in files)


def force_update_code_structure(prompt: Dict[str, Any]) -> str:
    # Get a list of all files in the current directory
    files = [path for path in os.listdir() if os.path.isfile(path)]

    # Initialize an empty code structure
    code_structure = {}

    model = os.getenv('SKELETON_MODEL', os.getenv('FAST_LLM_MODEL', 'gpt-3.5-turbo'))
    max_tokens = os.getenv('SKELETONM_TOKEN_LIMIT', os.getenv('FAST_TOKEN_LIMIT', 1500))
    temperature = os.getenv('SKELETON_TEMPERATURE', os.getenv('TEMPERATURE', 0.5))

    # Generate descriptions for all files
    for file in files:
        # Call the OpenAI API for chat completion to generate a file description
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are an assistant that generates descriptions of Python code files. Please describe the following file: {file}",
                },
                {
                    "role": "user",
                    "content": open(file).read(),
                },
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        # Add the generated description to the code structure
        code_structure[file] = response.choices[0].message['content']

    # Save the updated code structure to the file
    save_code_structure(code_structure)

    # Return the new file descriptions
    return "\n".join(f"{file}: {description}" for file, description in code_structure.items())
