from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
import threading
import os

from engine import AudioEngine
from stt import SpeechToText
from translator import Translator, VoiceSynthesizer
from download_models import MODELS, download_file

# UI Layout Definition
KV = """
<InterpreterUI>:
    orientation: 'vertical'
    canvas.before:
        Color:
            rgba: (0.1, 0.1, 0.1, 1)
        Rectangle:
            size: self.size
            pos: self.pos

    ScrollView:
        BoxLayout:
            id: foreign_pane
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: [10, 10]
            spacing: 5
            canvas.before:
                Color:
                    rgba: (0.2, 0.1, 0, 0.3) if root.is_listening else (0,0,0,0)
                Rectangle:
                    size: self.size
                    pos: self.pos

    Widget:
        size_hint_y: None
        height: '4dp'
        canvas:
            Color:
                rgba: (0, 0.8, 0, 1) if root.is_listening else (0.2, 0.2, 0.2, 1)
            Rectangle:
                pos: self.pos
                size: self.size

    ScrollView:
        BoxLayout:
            id: user_pane
            orientation: 'vertical'
            size_hint_y: None
            height: self.minimum_height
            padding: [10, 10]
            spacing: 5
            canvas.before:
                Color:
                    rgba: (0, 0.1, 0.2, 0.3) if root.is_listening else (0,0,0,0)
                Rectangle:
                    size: self.size
                    pos: self.pos

    Label:
        text: root.status_text
        size_hint_y: None
        height: '30dp'
        font_size: '12sp'
        color: (0.7, 0.7, 0.7, 1)
"""

class InterpreterUI(BoxLayout):
    is_listening = BooleanProperty(False)
    status_text = StringProperty("Initializing models...")

    def update_chat(self, side, text):
        Clock.schedule_once(lambda dt: self._update_chat_ui(side, text))

    def _update_chat_ui(self, side, text):
        label = Label(
            text=text, 
            size_hint_y=None, 
            text_size=(self.width * 0.9, None),
            halign='left',
            valign='middle'
        )
        label.bind(texture_size=label.setter('size'))
        if side == 'top':
            self.ids.foreign_pane.add_widget(label)
        else:
            self.ids.user_pane.add_widget(label)

class InterpreterApp(App):
    def build(self):
        Builder.load_string(KV)
        self.ui = InterpreterUI()
        return self.ui

    def on_start(self):
        if not os.path.exists("models"):
            os.makedirs("models")
        threading.Thread(target=self.initial_setup, daemon=True).start()

    def initial_setup(self):
        # 1. Download missing models
        for name, url in MODELS.items():
            if not os.path.exists(os.path.join("models", name)):
                self.ui.status_text = f"Downloading {name}..."
                download_file(url, name)
        
        # 2. Load Models
        self.ui.status_text = "Loading AI models..."
        self.stt = SpeechToText()
        self.translator = Translator()
        self.tts = VoiceSynthesizer()
        
        # 3. Start Audio Engine
        self.ui.status_text = "Ready"
        self.audio_engine = AudioEngine(stt_callback=self.process_pipeline)
        threading.Thread(target=self.audio_engine.start_stream, daemon=True).start()
        Clock.schedule_interval(self.update_status, 0.1)

    def update_status(self, dt):
        self.ui.is_listening = self.audio_engine.is_recording

    def process_pipeline(self, audio_data):
        # 1. STT
        transcription = self.stt.transcribe(audio_data)
        if not transcription: return
        self.ui.update_chat('bottom', f"Detected: {transcription}")
        
        # 2. LLM Translation
        translation = self.translator.translate(transcription)
        self.ui.update_chat('top', translation)
        
        # 3. TTS
        self.tts.speak(translation)

if __name__ == "__main__":
    InterpreterApp().run()
