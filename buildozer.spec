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

# (str) Custom environment variables to set during build
env.export = CFLAGS="-IC:\Users\aviel/.buildozer/android/platform/android-ndk-r25b/sysroot/usr/include/aarch64-linux-android -D__ANDROID_API__=21", LDFLAGS="-LC:\Users\aviel/.buildozer/android/platform/android-ndk-r25b/sysroot/usr/lib/aarch64-linux-android/21", CC="C:\Users\aviel/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android21-clang", CXX="C:\Users\aviel/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/aarch64-linux-android21-clang++", AR="C:\Users\aviel/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-ar", RANLIB="C:\Users\aviel/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-ranlib", STRIP="C:\Users\aviel/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/llvm-strip", LD="C:\Users\aviel/.buildozer/android/platform/android-ndk-r25b/toolchains/llvm/prebuilt/linux-x86_64/bin/ld", SKBUILD_CMAKE_ARGS="-DGGML_VULKAN=OFF -DGGML_CPU_ARM_V8A=ON -DLLAMA_NATIVE=OFF -DLLAMA_BUILD_SERVER=OFF -DCMAKE_SYSTEM_NAME=Android -DCMAKE_ANDROID_ARCH_ABI=arm64-v8a -DCMAKE_SYSTEM_VERSION=21"

# (list) Application requirements
# Note: torch is huge, swapped for onnxruntime
requirements = python3, kivy, android, plyer, numpy, llama-cpp-python, requests, tqdm

# (str) Custom source folders for p4a recipes
# p4a.local_recipes = ./recipes

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


