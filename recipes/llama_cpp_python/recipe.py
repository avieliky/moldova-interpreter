from pythonforandroid.recipe import CppCompiledComponentsPythonRecipe
from pythonforandroid.util import current_directory
from os.path import join
import os

class LlamaCppPythonRecipe(CppCompiledComponentsPythonRecipe):
    version = 'v0.3.7'
    url = 'https://github.com/abetlen/llama-cpp-python/archive/refs/tags/{version}.tar.gz'
    depends = ['setuptools', 'numpy']

    def get_recipe_env(self, arch):
        env = super().get_recipe_env(arch)
        # Force Vulkan Support
        env['GGML_VULKAN'] = '1'
        # NDK specific flags for Snapdragon 8 Gen 3
        env['CFLAGS'] += ' -O3 -fPIC'
        env['CXXFLAGS'] += ' -O3 -fPIC -std=c++17'
        return env

    def build_arch(self, arch):
        # We need to ensure llama.cpp is built within the context of the NDK
        with current_directory(self.get_build_dir(arch.arch)):
            env = self.get_recipe_env(arch)
            # Use pip's setup logic but with our NDK environment
            self.setup_libs(arch)
            super().build_arch(arch)

recipe = LlamaCppPythonRecipe()
