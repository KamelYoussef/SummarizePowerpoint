import ollama

response = ollama.chat(
    model='gemma3',
    messages=[
        {
            "role": "user",
            "content": "What is in this image?",
            "images": ["./your_image.jpg"]
        }
    ]
)

print(response["message"]["content"])
