import numpy as np
import sounddevice as sd
import torch
import time
from silero_vad import load_silero_vad, get_speech_timestamps

class AudioEngine:
    def __init__(self, stt_callback, fs=16000):
        self.stt_callback = stt_callback
        self.fs = fs
        self.vad_model = load_silero_vad()
        self.buffer = []
        self.is_recording = False
        self.silence_start_time = None
        self.speech_start_time = None
        
        # VAD Parameters
        self.speech_threshold = 0.5  # ms of speech to start
        self.silence_threshold = 1.0  # ms of silence to finalize
        
    def process_audio(self, indata, frames, time_info, status):
        if status:
            print(f"Audio Error: {status}")
            
        # Convert to float32 if needed
        audio_float32 = indata.flatten().astype(np.float32)
        
        # Silero VAD expects torch tensor
        audio_tensor = torch.from_numpy(audio_float32)
        
        # Simple speech detection
        speech_probs = self.vad_model(audio_tensor, self.fs).item()
        
        if speech_probs > 0.5:
            if not self.is_recording:
                if self.speech_start_time is None:
                    self.speech_start_time = time.time()
                elif time.time() - self.speech_start_time > self.speech_threshold:
                    print("VAD: Recording started...")
                    self.is_recording = True
                    self.buffer.append(audio_float32)
            else:
                self.buffer.append(audio_float32)
                self.silence_start_time = None
        else:
            if self.is_recording:
                self.buffer.append(audio_float32)
                if self.silence_start_time is None:
                    self.silence_start_time = time.time()
                elif time.time() - self.silence_start_time > self.silence_threshold:
                    print("VAD: Recording finalized.")
                    self.finalize_chunk()
            else:
                self.speech_start_time = None

    def finalize_chunk(self):
        if not self.buffer:
            return
            
        full_audio = np.concatenate(self.buffer)
        self.is_recording = False
        self.buffer = []
        self.silence_start_time = None
        self.speech_start_time = None
        
        # Trigger STT in a separate thread/callback
        self.stt_callback(full_audio)

    def start_stream(self):
        print("Starting continuous audio stream...")
        with sd.InputStream(samplerate=self.fs, channels=1, callback=self.process_audio, blocksize=512):
            while True:
                sd.sleep(100)
