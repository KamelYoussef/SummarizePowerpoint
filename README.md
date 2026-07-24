for segment in segments:
    seg_start = segment["start"]
    seg_end = segment["end"]
    text = segment["text"]
    
    # Get ALL speakers in this segment with their time ranges
    speaker_ranges = {}
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if turn.start < seg_end and turn.end > seg_start:
            # Overlap found
            overlap_start = max(turn.start, seg_start)
            overlap_end = min(turn.end, seg_end)
            
            if speaker not in speaker_ranges:
                speaker_ranges[speaker] = []
            speaker_ranges[speaker].append((overlap_start, overlap_end))
    
    # Format output
    if speaker_ranges:
        speakers_str = ", ".join([f"Speaker {s}" for s in speaker_ranges.keys()])
        print(f"[{seg_start:.2f}s - {seg_end:.2f}s] {speakers_str}: {text}")
    else:
        print(f"[{seg_start:.2f}s - {seg_end:.2f}s] [Unknown]: {text}")
