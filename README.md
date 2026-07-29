def to_wav(input_path: str) -> str:
    """Convert any audio file to a clean 16kHz mono WAV via ffmpeg."""
    tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", input_path,
            "-ar", "16000", "-ac", "1",
            tmp_wav,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return tmp_wav
