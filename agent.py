import ollama
from tools import calculator


def run_agent(user_input):

    response = ollama.chat(
        model="llama3.2:latest",
        messages=[
            {
                "role": "system",
                "content": """
You are an AI agent.

You can use a calculator tool when the user asks
for a mathematical calculation.

If calculation is required, identify the mathematical
expression that needs to be calculated.
"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    return response["message"]["content"]


if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        answer = run_agent(user_input)
        print("\nAgent:", answer)