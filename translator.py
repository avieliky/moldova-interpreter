from llama_cpp import Llama
import os

class Translator:
    def __init__(self, model_path="models/Gemma-2-9B-It-Q4_K_M.gguf"):
        # Check for Vulkan support or fallback to CPU
        self.llm = Llama(
            model_path=model_path,
            n_gpu_layers=-1,  # Offload all layers to GPU
            n_ctx=2048,
            verbose=False,
            # Force Vulkan if available, though llama-cpp-python usually handles this
        )
        
        self.system_prompt = (
            "You are a real-time interpreter in Moldova. "
            "The input will be Romanian with local regionalisms and Russian loanwords. "
            "Directly translate the INTENT to natural English. "
            "If the input is English, translate it to standard Romanian."
        )

    def translate(self, text):
        print(f"LLM: Translating '{text}'...")
        response = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.2,
            max_tokens=256
        )
        return response['choices'][0]['message']['content'].strip()

# Placeholder for TTS
class VoiceSynthesizer:
    def __init__(self):
        # We will use Piper-TTS here
        pass
        
    def speak(self, text):
        print(f"TTS: Speaking '{text}'")
        # Piper integration logic
        pass
