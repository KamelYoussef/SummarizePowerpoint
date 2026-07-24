timeline.sort(key=lambda x: x["start"])

# 5. Generate merged transcript
output = []
current_speaker = None
current_text = []

for item in timeline:
    if item["type"] == "speaker":
        current_speaker = item["speaker"]
    elif item["type"] == "text":
        speaker = current_speaker if current_speaker else "Unknown"
        
        # If speaker changed, save previous speaker's text
        if output and output[-1]["speaker"] != speaker:
            current_text = []
        
        # Add text to current speaker's group
        if output and output[-1]["speaker"] == speaker:
            output[-1]["text"].append(item["content"])
        else:
            output.append({"speaker": speaker, "text": [item["content"]]})

# Print clean merged transcript
for entry in output:
    merged_text = " ".join(entry["text"])
    print(f"[Speaker {entry['speaker']}]: {merged_text}")

# Optional: Save to file
with open("transcript.txt", "w") as f:
    for entry in output:
        merged_text = " ".join(entry["text"])
        f.write(f"[Speaker {entry['speaker']}]: {merged_text}\n")
