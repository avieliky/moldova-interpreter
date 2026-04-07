import numpy as np
import sounddevice as sd
import onnxruntime as ort
import time
import threading

class AudioEngine:
    def __init__(self, stt_callback, fs=16000):
        self.stt_callback = stt_callback
        self.fs = fs
        # Load Silero VAD ONNX model
        self.session = ort.InferenceSession("models/silero_vad.onnx")
        self.h = np.zeros((2, 1, 64), dtype=np.float32)
        self.c = np.zeros((2, 1, 64), dtype=np.float32)
        
        self.buffer = []
        self.is_recording = False
        self.silence_start_time = None
        self.speech_start_time = None
        
        self.speech_threshold = 0.4
        self.silence_threshold = 0.8

    def process_audio(self, indata, frames, time_info, status):
        audio_float32 = indata.flatten().astype(np.float32)
        
        # Silero ONNX Input
        ort_inputs = {
            'input': audio_float32.reshape(1, -1),
            'sr': np.array([self.fs], dtype=np.int64),
            'h': self.h,
            'c': self.c
        }
        
        out, self.h, self.c = self.session.run(None, ort_inputs)
        speech_prob = out[0][0]

        if speech_prob > 0.5:
            if not self.is_recording:
                if self.speech_start_time is None:
                    self.speech_start_time = time.time()
                elif time.time() - self.speech_start_time > 0.3:
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
                    self.finalize_chunk()

    def finalize_chunk(self):
        if not self.buffer: return
        full_audio = np.concatenate(self.buffer)
        self.is_recording = False
        self.buffer = []
        self.silence_start_time = None
        self.speech_start_time = None
        threading.Thread(target=self.stt_callback, args=(full_audio,), daemon=True).start()

    def start_stream(self):
        with sd.InputStream(samplerate=self.fs, channels=1, callback=self.process_audio, blocksize=512):
            while True: sd.sleep(100)
