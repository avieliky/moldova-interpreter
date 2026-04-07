from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.properties import BooleanProperty, StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
import threading
from engine import AudioEngine

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

    # Foreign Speaker Pane (Top)
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

    # Glow Indicator for VAD
    Widget:
        size_hint_y: None
        height: '4dp'
        canvas:
            Color:
                rgba: (0, 0.8, 0, 1) if root.is_listening else (0.2, 0.2, 0.2, 1)
            Rectangle:
                pos: self.pos
                size: self.size

    # User Pane (Bottom)
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

    # Status Bar
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
        # side: 'top' (Foreign) or 'bottom' (User)
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

from download_models import MODELS, download_file
import os

class InterpreterApp(App):
    def build(self):
        Builder.load_string(KV)
        self.ui = InterpreterUI()
        return self.ui

    def on_start(self):
        # Ensure models are present
        if not os.path.exists("models"):
            os.makedirs("models")
            
        threading.Thread(target=self.initial_download, daemon=True).start()

    def initial_download(self):
        for name, url in MODELS.items():
            if not os.path.exists(os.path.join("models", name)):
                self.ui.status_text = f"Downloading {name}..."
                download_file(url, name)
        
        self.ui.status_text = "Models loaded. Starting..."
        # Start Audio Engine after models are verified
        self.audio_engine = AudioEngine(stt_callback=self.process_stt)
        threading.Thread(target=self.audio_engine.start_stream, daemon=True).start()
        
        # Monitor VAD status for the UI glow
        Clock.schedule_interval(self.update_status, 0.1)

    def update_status(self, dt):
        self.ui.is_listening = self.audio_engine.is_recording
        if self.ui.is_listening:
            self.ui.status_text = "Listening..."
        else:
            self.ui.status_text = "Ready"

    def process_stt(self, audio_data):
        # This will be implemented based on your STT choice
        print("STT: Processing chunk...")
        pass

if __name__ == "__main__":
    InterpreterApp().run()
