from llama_cpp import Llama
import os
import subprocess
import sounddevice as sd
import numpy as np

class Translator:
    def __init__(self, model_path="models/Gemma-2-9B-It-Q4_K_M.gguf"):
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1, 
            n_ctx=2048,
            verbose=False,
        )
        self.system_prompt = (
            "You are a real-time interpreter in Moldova. "
            "The input will be Romanian with local regionalisms and Russian loanwords. "
            "Directly translate the INTENT to natural English. "
            "If the input is English, translate it to standard Romanian."
        )

    def translate(self, text):
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.2,
            max_tokens=256
        )
        return response['choices'][0]['message']['content'].strip()

class VoiceSynthesizer:
    def __init__(self):
        # We assume 'piper' is installed and in the path, or use the onnx model
        self.ro_model = "models/ro_RO-mihai-low.onnx"
        self.en_model = "models/en_US-lessac-medium.onnx"

    def speak(self, text, is_romanian=False):
        model = self.ro_model if is_romanian else self.en_model
        # Call piper via subprocess for immediate playback to a virtual sink or file
        # This is a common way to use Piper-TTS on mobile
        try:
            cmd = f"echo '{text}' | piper --model {model} --output_raw"
            audio_raw = subprocess.check_output(cmd, shell=True)
            audio_np = np.frombuffer(audio_raw, dtype=np.int16).astype(np.float32) / 32768.0
            sd.play(audio_np, 22050)
        except Exception as e:
            print(f"TTS Error: {e}")
