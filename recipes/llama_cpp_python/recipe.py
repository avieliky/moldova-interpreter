from pythonforandroid.recipe import CompiledComponentsPythonRecipe
import os

class LlamaCppPythonRecipe(CompiledComponentsPythonRecipe):
    version = 'v0.3.7'
    url = 'https://github.com/abetlen/llama-cpp-python/archive/refs/tags/{version}.tar.gz'
    depends = ['setuptools', 'numpy']
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        
        # CRITICAL: Prevent llama.cpp from using -march=native
        # These are the specific flags that llama-cpp-python / scikit-build-core look for
        cmake_args = [
            "-DGGML_NATIVE=OFF",
            "-DGGML_OPENMP=OFF",
            "-DGGML_VULKAN=ON",
            "-DGGML_CPU_ARM_V8A=ON",
            "-DGGML_CPU_ALL_VARIANTS=ON",
            "-DLLAMA_NATIVE=OFF",
            "-DLLAMA_BUILD_SERVER=OFF",
            f"-DCMAKE_SYSTEM_NAME=Android",
            f"-DCMAKE_ANDROID_ARCH_ABI={arch.arch}",
            "-DCMAKE_SYSTEM_VERSION=21",
        ]
        
        # Join them into the environment variables used by pip/scikit-build
        arg_str = " ".join(cmake_args)
        env['CMAKE_ARGS'] = arg_str
        env['SKBUILD_CMAKE_ARGS'] = arg_str
        
        # Ensure we don't use host optimizations
        env['GGML_NATIVE'] = 'OFF'
        env['LLAMA_NATIVE'] = 'OFF'
        
        return env

recipe = LlamaCppPythonRecipe()
