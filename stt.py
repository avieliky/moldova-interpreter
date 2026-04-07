from kivy.utils import platform

class SpeechToText:
    def __init__(self):
        self.is_android = platform == 'android'
        if self.is_android:
            try:
                from jnius import autoclass
                from android.permissions import request_permissions, Permission
                request_permissions([Permission.RECORD_AUDIO])
            except ImportError:
                pass
                
    def transcribe(self, audio_data=None):
        if not self.is_android:
            return "Not on Android."
        return "[Android Native STT Active]"
