from pythonforandroid.recipe import PythonRecipe
import os

class LlamaCppPythonRecipe(PythonRecipe):
    name = 'llama-cpp-python'
    version = '0.3.7'
    url = 'https://github.com/abetlen/llama-cpp-python/archive/refs/tags/v{version}.tar.gz'
    depends = ['setuptools', 'numpy']
    call_hostpython_via_targetpython = False

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)

        cmake_args = [
            "-DGGML_NATIVE=OFF",
            "-DGGML_OPENMP=OFF",
            "-DGGML_VULKAN=OFF",
            "-DGGML_CPU_ARM_V8A=ON",
            "-DGGML_CPU_ALL_VARIANTS=ON",
            "-DLLAMA_NATIVE=OFF",
            "-DLLAMA_BUILD_SERVER=OFF",
            f"-DCMAKE_SYSTEM_NAME=Android",
            f"-DCMAKE_ANDROID_ARCH_ABI={arch.arch}",
            "-DCMAKE_SYSTEM_VERSION=21",
        ]

        env['CMAKE_ARGS'] = " ".join(cmake_args)
        env['SKBUILD_CMAKE_ARGS'] = " ".join(cmake_args)
        env['GGML_NATIVE'] = 'OFF'
        env['LLAMA_NATIVE'] = 'OFF'

        return env

recipe = LlamaCppPythonRecipe()
