from llama_cpp import Llama
from kivy.utils import platform

class Translator:
    def __init__(self, model_path='models/gemma-2-2b-it-Q4_K_M.gguf'):
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=0,
            n_ctx=2048,
            verbose=False,
        )
        self.system_prompt = (
            'You are a real-time intent interpreter for a Moldovan speaker. '
            'The input will be a mix of Romanian, Russian, and possibly Italian or regionalisms. '
            'Do not translate word-for-word. Understand the underlying phrase, thought, or intent, '
            'and output ONLY the natural English translation of that intent. '
        )

    def translate(self, text):
        try:
            response = self.llm.create_chat_completion(
                messages=[
                    {'role': 'system', 'content': self.system_prompt},
                    {'role': 'user', 'content': text}
                ],
                temperature=0.2,
                max_tokens=256
            )
            return response['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(f'Llama Translation Error: {e}')
            return f'[Translation Error: {e}]'

class VoiceSynthesizer:
    def __init__(self):
        self.is_android = platform == 'android'
        if self.is_android:
            try:
                from plyer import tts
                self.tts = tts
            except ImportError:
                self.tts = None

    def speak(self, text, is_romanian=False):
        if self.is_android and hasattr(self, 'tts') and self.tts:
            try:
                self.tts.speak(text)
            except Exception as e:
                print(f'Plyer TTS error: {e}')
        else:
            print(f'TTS (Simulation): {text}')
