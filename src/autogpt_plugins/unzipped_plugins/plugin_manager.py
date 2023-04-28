import importlib
import subprocess
from pathlib import Path
import sys


class PluginManager:
    @staticmethod
    def install_plugin_requirements(plugins_dir: Path):
        # Find all dirs that contain a requirements.txt file.
        for path in plugins_dir.rglob("requirements.txt"):
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "-r", path]
                )
            except KeyError:
                continue

    @staticmethod
    def load_unzipped_plugins(plugins_dir: Path):
        unzipped_plugins = []

        # Find all dirs that contain a __init__.py file.
        for path in plugins_dir.rglob("__init__.py"):
            if "AllowUnzippedPlugins" in str(path):
                continue

            print(f"Found module '{path.parent.name}' at: {path}")

            spec = importlib.util.spec_from_file_location(path.parent.name, str(path))
            loaded_module = importlib.util.module_from_spec(spec)

            for key in dir(loaded_module):
                if key.startswith("__"):
                    continue
                a_module = getattr(loaded_module, key)
                a_keys = dir(a_module)
                if (
                    "_abc_impl" in a_keys
                    and a_module.__name__ != "AutoGPTPluginTemplate"
                ):
                    spec.loader.exec_module(loaded_module)
                    sys.modules[path.parent.name] = loaded_module
                    unzipped_plugins.append(a_module())

        return unzipped_plugins
