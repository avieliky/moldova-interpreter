import os
import requests
from tqdm import tqdm

MODELS = {
    "silero_vad.onnx": "https://github.com/snakers4/silero-vad/raw/master/files/silero_vad.onnx",
    "Gemma-2-9B-It-Q4_K_M.gguf": "https://huggingface.co/bartowski/gemma-2-9b-it-GGUF/resolve/main/gemma-2-9b-it-Q4_K_M.gguf",
    "whisper-large-v3-turbo-ct2/model.bin": "https://huggingface.co/Systran/faster-whisper-large-v3-turbo/resolve/main/model.bin",
    "whisper-large-v3-turbo-ct2/config.json": "https://huggingface.co/Systran/faster-whisper-large-v3-turbo/resolve/main/config.json",
    "whisper-large-v3-turbo-ct2/vocabulary.json": "https://huggingface.co/Systran/faster-whisper-large-v3-turbo/resolve/main/vocabulary.json",
    "piper-ro-low.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/ro/ro_RO/mihai/low/ro_RO-mihai-low.onnx",
    "piper-ro-low.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/ro/ro_RO/mihai/low/ro_RO-mihai-low.onnx.json",
    "piper-en-medium.onnx": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx",
    "piper-en-medium.onnx.json": "https://huggingface.co/rhasspy/piper-voices/resolve/main/en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"
}

def download_file(url, filename):
    path = os.path.join("models", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
        
    print(f"Downloading {filename}...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(path, "wb") as f, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for data in response.iter_content(chunk_size=1024):
            size = f.write(data)
            bar.update(size)

if __name__ == "__main__":
    if not os.path.exists("models"):
        os.makedirs("models")
    for name, url in MODELS.items():
        download_file(url, name)
