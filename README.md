import whisper
import torch
import librosa
from pyannote.audio import Pipeline

# 1. Load audio
audio, sample_rate = librosa.load("file.mp3", sr=16000)
waveform = torch.tensor(audio).float()

# 2. Transcription
model = whisper.load_model("small", device="cpu")
result = whisper.transcribe(model, "file.mp3")
segments = result["segments"]

# 3. Speaker diarization
pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    use_auth_token="YOUR_HF_TOKEN"
)

diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})

# 4. Create merged timeline of text + speakers
timeline = []

# Add all text chunks with their times
for segment in segments:
    timeline.append({
        "type": "text",
        "start": segment["start"],
        "end": segment["end"],
        "content": segment["text"].strip()
    })

# Add all speaker turns with their times
for turn, _, speaker in diarization.itertracks(yield_label=True):
    timeline.append({
        "type": "speaker",
        "start": turn.start,
        "end": turn.end,
        "speaker": speaker
    })

# Sort by start time
timeline.sort(key=lambda x: x["start"])

# 5. Generate clean transcript
current_speaker = None
output = []

for item in timeline:
    if item["type"] == "speaker":
        current_speaker = item["speaker"]
    elif item["type"] == "text":
        # Check if speaker changed at or before this text
        speaker_str = f"[Speaker {current_speaker}]" if current_speaker else "[Unknown]"
        output.append(f"{speaker_str}: {item['content']}")

# Print clean transcript
transcript = "\n".join(output)
print(transcript)

# Optional: Save to file
with open("transcript.txt", "w") as f:
    f.write(transcript)
