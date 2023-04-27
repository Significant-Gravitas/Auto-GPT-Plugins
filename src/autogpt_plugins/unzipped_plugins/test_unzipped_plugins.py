from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
import importlib.util

# We're in test mode
import os
os.environ['TEST_MODE'] = 'true'

from autogpt_plugins.unzipped_plugins import AutoGPTAllowUnzippedPlugins
from auto_gpt_plugin_template import AutoGPTPluginTemplate


class TestData:
    _abc_impl = True
            
def test_load_unzipped_plugins():
    with patch("autogpt_plugins.unzipped_plugins.Path.rglob") as rglob_mock, patch(
        "autogpt_plugins.unzipped_plugins.importlib.util.spec_from_file_location"
    ) as spec_from_file_location_mock, patch(
        "autogpt_plugins.unzipped_plugins.importlib.util.module_from_spec"
    ) as module_from_spec_mock:
        rglob_mock.return_value = [
            Path("plugins/__init__.py"),
            Path("plugins/dummy_plugin/src/__init__.py"),
            Path("plugins/plugin1/__init__.py"),
        ]

        spec_mock = MagicMock()
        spec_from_file_location_mock.return_value = spec_mock

        # Mock load_module
        class MockLoadedModule:
            AutoGPTPluginTemplate = AutoGPTPluginTemplate
            PluginClass = TestData
            
        loaded_module_mock = MockLoadedModule()
        module_from_spec_mock.return_value = loaded_module_mock

        plugin_instance = AutoGPTAllowUnzippedPlugins()
        unzipped_plugins = plugin_instance.load_unzipped_plugins()
        assert len(unzipped_plugins) == 3
        assert unzipped_plugins[0].__class__.__name__ == "TestData"
        assert "plugin1" in sys.modules