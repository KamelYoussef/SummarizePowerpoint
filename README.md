# Split segments by speaker boundaries
output_chunks = []

for segment in segments:
    seg_start = segment["start"]
    seg_end = segment["end"]
    text = segment["text"]
    
    # Get speaker timeline for this segment
    speaker_timeline = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if turn.start < seg_end and turn.end > seg_start:
            overlap_start = max(turn.start, seg_start)
            overlap_end = min(turn.end, seg_end)
            speaker_timeline.append({
                "start": overlap_start,
                "end": overlap_end,
                "speaker": speaker
            })
    
    # Sort by time
    speaker_timeline.sort(key=lambda x: x["start"])
    
    # Print with speaker transitions
    if speaker_timeline:
        for i, turn in enumerate(speaker_timeline):
            print(f"[{turn['start']:.2f}s - {turn['end']:.2f}s] Speaker {turn['speaker']}: {text}")
    else:
        print(f"[{seg_start:.2f}s - {seg_end:.2f}s] [Unknown]: {text}")
