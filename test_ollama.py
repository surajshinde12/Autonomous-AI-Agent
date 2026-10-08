import ollama

response = ollama.chat(
    model="llama3.2:latest",
    messages=[
        {
            "role": "user",
            "content": "Explain in one sentence what an AI agent is."
        }
    ]
)

print(response["message"]["content"])