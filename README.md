from jupyter_ai.magics import register_backend
import ollama

@register_backend(name="ollama", description="Ollama Local LLM Backend")
def ollama_backend(prompt, model="llama2"):
    response = ollama.complete(prompt=prompt, model=model)
    return response["text"]
