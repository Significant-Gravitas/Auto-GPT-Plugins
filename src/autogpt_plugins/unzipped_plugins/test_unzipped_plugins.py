from unittest.mock import MagicMock, call, patch
from pathlib import Path
import sys
import importlib.util

# We're in test mode
import os

from .plugin_manager import PluginManager

os.environ["TEST_MODE"] = "true"

from auto_gpt_plugin_template import AutoGPTPluginTemplate


class TestData:
    _abc_impl = True


def test_load_unzipped_plugins():
    with patch.object(Path, "rglob") as rglob_mock, patch(
        "importlib.util.spec_from_file_location"
    ) as spec_from_file_location_mock, patch(
        "importlib.util.module_from_spec"
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

        from . import AutoGPTAllowUnzippedPlugins

        unzipped_plugins = PluginManager.load_unzipped_plugins(Path("./"))
        assert len(unzipped_plugins) == 3
        assert unzipped_plugins[0].__class__.__name__ == "TestData"
        assert "plugin1" in sys.modules


def test_install_plugin_requirements():
    with patch.object(Path, "rglob") as mock_rglob, patch(
        "subprocess.check_call"
    ) as mock_subprocess_check_call:
        mock_rglob.return_value = [
            Path("./plugin1/requirements.txt"),
            Path("./plugin2/requirements.txt"),
        ]

        PluginManager.install_plugin_requirements(Path("./plugins"))

        expected_calls = [
            call([sys.executable, "-m", "pip", "install", "-r", path])
            for path in mock_rglob.return_value
        ]
        mock_subprocess_check_call.assert_has_calls(expected_calls, any_order=True)

        mock_subprocess_check_call.side_effect = KeyError("Test KeyError")
        PluginManager.install_plugin_requirements(Path("./plugins"))

        assert mock_subprocess_check_call.call_count == len(expected_calls) * 2
