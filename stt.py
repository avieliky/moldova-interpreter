from faster_whisper import WhisperModel
import os

class SpeechToText:
    def __init__(self, model_size="large-v3-turbo", download_root="models/whisper-large-v3-turbo-ct2"):
        # We let faster-whisper handle the download automatically
        # This is more reliable than manual downloads
        self.model = WhisperModel(
            model_size, 
            device="cpu", 
            compute_type="int8",
            download_root=download_root
        )

    def transcribe(self, audio_data):
        print("STT: Transcribing chunk...")
        segments, info = self.model.transcribe(
            audio_data, 
            beam_size=5, 
            language=None, # Allow auto-detect for Moldovan mix (Ro, Ru, It)
            task="transcribe"
        )
        
        full_text = " ".join([segment.text for segment in segments])
        return full_text.strip()
