from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe
import os

class LlamaCppPythonRecipe(CppCompiledComponentsPythonRecipe):
    version = 'v0.3.7'
    url = 'https://github.com/abetlen/llama-cpp-python/archive/refs/tags/{version}.tar.gz'
    depends = ['setuptools', 'numpy']

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        
        # Disable auto-detection of 'native' architecture which fails in cross-compile
        env['GGML_NATIVE'] = 'OFF'
        env['GGML_OPENMP'] = 'OFF' # OpenMP can be tricky on Android, disabling for stability
        
        # Enable Vulkan for your S24 Ultra GPU
        env['GGML_VULKAN'] = '1'
        
        # Target ARM64 explicitly
        env['GGML_CPU_ALL_VARIANTS'] = '1'
        
        # Point to Android's Vulkan loader
        env['CMAKE_ARGS'] = (
            f"-DGGML_VULKAN=ON "
            f"-DGGML_NATIVE=OFF "
            f"-DGGML_CPU_ARM_V8A=ON "
            f"-DCMAKE_SYSTEM_NAME=Android "
            f"-DCMAKE_ANDROID_ARCH_ABI={arch.arch} "
            f"-DCMAKE_SYSTEM_VERSION=21 "
        )
        
        return env

recipe = LlamaCppPythonRecipe()
