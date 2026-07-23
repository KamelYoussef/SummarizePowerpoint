for segment in segments:
    speakers = []
    for turn, _, speaker in diarization.itertracks(yield_label=True):
        if turn.start < segment.end and turn.end > segment.start:
            speakers.append(speaker)
    
    speaker_str = f"[Speaker {list(set(speakers))[0]}]" if speakers else "[Unknown]"
    print(f"[{segment.start:.2f}s] {speaker_str}: {segment.text}")
