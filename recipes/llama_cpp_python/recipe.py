from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe
import os

class LlamaCppPythonRecipe(CppCompiledComponentsPythonRecipe):
    version = 'v0.3.7'
    url = 'https://github.com/abetlen/llama-cpp-python/archive/refs/tags/{version}.tar.gz'
    depends = ['setuptools', 'numpy']

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        
        # Completely disable native detection and OpenMP (which can be unstable)
        env['GGML_NATIVE'] = 'OFF'
        env['GGML_OPENMP'] = 'OFF'
        env['GGML_VULKAN'] = '1'
        
        # Force the CMake arguments directly into the environment
        env['CMAKE_ARGS'] = (
            "-DGGML_NATIVE=OFF "
            "-DGGML_CPU_ARM_V8A=ON "
            "-DGGML_VULKAN=ON "
            "-DGGML_OPENMP=OFF "
            "-DLLAMA_BUILD_SERVER=OFF "
        )
        
        # Override any internal scikit-build flags
        env['SKBUILD_CMAKE_ARGS'] = env['CMAKE_ARGS']
        
        return env

recipe = LlamaCppPythonRecipe()
