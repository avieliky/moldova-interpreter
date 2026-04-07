from llama_cpp import Llama
import os
import sounddevice as sd
import numpy as np
from piper import PiperVoice

class Translator:
    def __init__(self, model_path="models/gemma-2-2b-it-Q4_K_M.gguf"):
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=0, # Android CPU
            n_ctx=2048,
            verbose=False,
        )
        self.system_prompt = (
            "You are a real-time intent interpreter for a Moldovan speaker. "
            "The input will be a mix of Romanian, Russian, and possibly Italian or regionalisms. "
            "Do not translate word-for-word. Understand the underlying phrase, thought, or intent, "
            "and output ONLY the natural English translation of that intent. "
        )

    def translate(self, text):
        try:
            response = self.llm.create_chat_completion(
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": text}
                ],
                temperature=0.2,
                max_tokens=256
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f"Llama Translation Error: {e}")
            return f"[Translation Error: {e}]"

class VoiceSynthesizer:
    def __init__(self):
        self.ro_model = "models/ro_RO-mihai-medium.onnx"
        self.en_model = "models/en_US-lessac-medium.onnx"
        self.voices = {}

    def _get_voice(self, model_path):
        if model_path not in self.voices:
            if not os.path.exists(model_path):
                print(f"TTS Model {model_path} not found")
                return None
            try:
                self.voices[model_path] = PiperVoice.load(model_path)
            except Exception as e:
                print(f"Error loading TTS model {model_path}: {e}")
                return None
        return self.voices[model_path]

    def speak(self, text, is_romanian=False):
        model_path = self.ro_model if is_romanian else self.en_model
        voice = self._get_voice(model_path)
        if not voice: return
        
        try:
            # Collect audio chunks from synthesis
            audio_data = b"".join(voice.synthesize(text))
            audio_np = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
            sd.play(audio_np, voice.config.sample_rate)
        except Exception as e:
            print(f"TTS Synthesis Error: {e}")
