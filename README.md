def predict(self, context, model_input):
        # If input is a dict (JSON), this works directly.
        # If MLflow wraps it in a DataFrame (common in some deployments),
        # you can handle both cases:
        if isinstance(model_input, pd.DataFrame):
            data = model_input.to_dict(orient="records")[0]
        else:
            data = model_input

        # Now 'data' is your simple dict: {"audio_base64": "..."}
        audio_bytes = base64.b64decode(data['audio_base64'])
        
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name
        
        # Transcribe
        result = self.model.transcribe(tmp_path)
        os.remove(tmp_path)
        
        return {"text": result['text']}
