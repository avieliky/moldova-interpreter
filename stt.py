from faster_whisper import WhisperModel
import os

class SpeechToText:
    def __init__(self, model_path="models/whisper-large-v3-turbo-ct2"):
        # CPU setup - using 'auto' will detect multiple cores
        # 'int8' is used for ARM CPU optimization (NEON instructions)
        self.model = WhisperModel(
            model_path, 
            device="cpu", 
            compute_type="int8",
            local_files_only=True
        )

    def transcribe(self, audio_data):
        print("STT: Transcribing chunk...")
        # language=None allows auto-detection (useful for Romanian vs English)
        segments, info = self.model.transcribe(
            audio_data, 
            beam_size=5, 
            language="ro", # Force Romanian initially for better Moldovan detection
            task="transcribe"
        )
        
        full_text = " ".join([segment.text for segment in segments])
        return full_text.strip()
