# 5. Generate clean transcript - merge same speaker lines
current_speaker = None
current_text = []
output = []

for item in timeline:
    if item["type"] == "speaker":
        current_speaker = item["speaker"]
    elif item["type"] == "text":
        speaker = current_speaker if current_speaker else "Unknown"
        
        # If speaker changed, flush previous speaker's text
        if current_text and (not current_speaker or speaker != output[-1].split(":")[0].replace("[Speaker ", "").replace("]", "")):
            # Save previous speaker's combined text
            pass
        
        current_text.append(item["content"])

# Better approach - group by speaker
current_speaker = None
accumulated_text = []
output = []

for item in timeline:
    if item["type"] == "speaker":
        # If speaker changed, save previous speaker's text
        if accumulated_text and current_speaker is not None:
            speaker_str = f"[Speaker {current_speaker}]"
            combined = " ".join(accumulated_text)
            output.append(f"{speaker_str}: {combined}")
            accumulated_text = []
        
        current_speaker = item["speaker"]
    
    elif item["type"] == "text":
        if current_speaker is None:
            current_speaker = "Unknown"
        accumulated_text.append(item["content"])

# Don't forget the last speaker's accumulated text
if accumulated_text and current_speaker is not None:
    speaker_str = f"[Speaker {current_speaker}]"
    combined = " ".join(accumulated_text)
    output.append(f"{speaker_str}: {combined}")

# Print clean transcript
transcript = "\n".join(output)
print(transcript)

# Optional: Save to file
with open("transcript.txt", "w") as f:
    f.write(transcript)
