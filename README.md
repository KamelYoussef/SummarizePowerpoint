def predict(self, context, model_input: Dict[str, str]):
        audio_bytes = base64.b64decode(model_input['audio_base64'])

        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        # 1. Get the generator
        segments_gen, info = self.model.transcribe(tmp_path, language="fr", word_timestamps=True)
        
        # 2. Convert the generator to a list of serializable dictionaries
        segments_list = [
            {
                "start": s.start,
                "end": s.end,
                "text": s.text,
            }
            for s in segments_gen
        ]
        
        os.remove(tmp_path)

        # 3. Return the processed list
        return {
            "segments": segments_list,
            "info": {
                "language": info.language,
                "duration": info.duration
            }
        }
