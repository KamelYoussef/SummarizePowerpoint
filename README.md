"""
Transcribe French audio using Mistral's Voxtral Mini (3B), open-weight, Apache 2.0.

Install:
    pip install -U transformers
    pip install --upgrade "mistral-common[audio]"

Requires a GPU with ~9.5 GB VRAM (bf16/fp16). For CPU-only setups, consider
faster-whisper large-v3 instead, or the vLLM server route documented on
Voxtral's model card for lighter local inference.
"""

from transformers import VoxtralForConditionalGeneration, AutoProcessor
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
REPO_ID = "mistralai/Voxtral-Mini-3B-2507"

# Path or URL to your French audio file (wav/mp3/etc.)
AUDIO_PATH = "path/to/your/french_audio.mp3"


def transcribe(audio_path: str, language: str = "fr") -> str:
    processor = AutoProcessor.from_pretrained(REPO_ID)
    model = VoxtralForConditionalGeneration.from_pretrained(
        REPO_ID,
        torch_dtype=torch.bfloat16 if DEVICE == "cuda" else torch.float32,
        device_map=DEVICE,
    )

    inputs = processor.apply_transcription_request(
        language=language,
        audio=audio_path,
        model_id=REPO_ID,
    )
    inputs = inputs.to(DEVICE, dtype=torch.bfloat16 if DEVICE == "cuda" else torch.float32)

    outputs = model.generate(**inputs, max_new_tokens=500)
    decoded = processor.batch_decode(
        outputs[:, inputs.input_ids.shape[1]:], skip_special_tokens=True
    )
    return decoded[0]


if __name__ == "__main__":
    text = transcribe(AUDIO_PATH, language="fr")
    print("Transcription (FR):")
    print(text)
