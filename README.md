from gemma import gm
tokenizer = gm.text.Gemma3Tokenizer()
model = gm.nn.Gemma3_4B()

# Using ChatSampler or a similar prompt wrapper:
sampler = gm.text.ChatSampler(model=model, tokenizer=tokenizer)

# Provide images and text in interleaved content:
messages = [
    {"role": "system", "content": [{"type": "text", "text": "You’re an assistant."}]},
    {
      "role": "user",
      "content": [
        {"type": "image", "url": "path_or_url_to_image1.jpg"},
        {"type": "text", "text": "What’s in this image?"}
      ]
    }
]

response = sampler.sample_chat(messages, max_new_tokens=100)
print(response)
