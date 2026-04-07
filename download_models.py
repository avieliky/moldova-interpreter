import os
from huggingface_hub import hf_hub_download

MODELS = {
    "silero_vad.onnx": ("https://github.com/snakers4/silero-vad/raw/master/files/silero_vad.onnx", None),
    "gemma-2-2b-it-Q4_K_M.gguf": ("bartowski/gemma-2-2b-it-GGUF", "gemma-2-2b-it-Q4_K_M.gguf"),
    "ro_RO-mihai-medium.onnx": ("rhasspy/piper-voices", "ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx"),
    "ro_RO-mihai-medium.onnx.json": ("rhasspy/piper-voices", "ro/ro_RO/mihai/medium/ro_RO-mihai-medium.onnx.json"),
    "en_US-lessac-medium.onnx": ("rhasspy/piper-voices", "en/en_US/lessac/medium/en_US-lessac-medium.onnx"),
    "en_US-lessac-medium.onnx.json": ("rhasspy/piper-voices", "en/en_US/lessac/medium/en_US-lessac-medium.onnx.json"),
}

def download_all():
    if not os.path.exists("models"):
        os.makedirs("models")
        
    for local_name, (repo_or_url, filename) in MODELS.items():
        path = os.path.join("models", local_name)
        if os.path.exists(path):
            continue
            
        print(f"Downloading {local_name}...")
        if filename:
            # HuggingFace download
            hf_hub_download(
                repo_id=repo_or_url,
                filename=filename,
                local_dir="models",
                local_dir_use_symlinks=False
            )
            # Rename if necessary (hf_hub_download might save with full path)
            downloaded_path = os.path.join("models", filename)
            if os.path.exists(downloaded_path) and downloaded_path != path:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                os.rename(downloaded_path, path)
        else:
            # Direct URL download (like Silero)
            import requests
            r = requests.get(repo_or_url)
            with open(path, "wb") as f:
                f.write(r.content)

if __name__ == "__main__":
    download_all()
