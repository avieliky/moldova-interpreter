[app]
# (str) Title of your application
title = Moldova Interpreter

# (str) Package name
package.name = moldovainterpreter

# (str) Package domain (needed for android packaging)
package.domain = org.avieliky

# (str) Version of your application
version = 0.1

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let's include the models)
source.include_exts = py,png,jpg,kv,json,onnx,gguf,bin,txt

# (list) Application requirements
# Note: torch is huge, swapped for onnxruntime
requirements = python3, kivy, numpy, sounddevice, onnxruntime, faster-whisper, llama-cpp-python, requests, tqdm, soundfile

# (str) Custom source folders for p4a recipes
p4a.local_recipes = ./recipes

# (list) Permissions
android.permissions = RECORD_AUDIO, MODIFY_AUDIO_SETTINGS, WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE, INTERNET

# (int) Target Android API, should be as high as possible.
android.api = 34

# (str) Android build-tools version to use
android.build_tools_version = 34.0.0

# (int) Minimum API your APK will support.

android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use the Vulkan feature
android.extra_manifest_xml_contents = <uses-feature android:name="android.hardware.vulkan.version" android:required="true" />

# (list) Android architectures to build for
android.archs = arm64-v8a

# (list) List of service to declare
# We can run the audio engine as a background service
# services = InterpreterEngine:engine.py

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = false, 1 = true)
warn_on_root = 1
