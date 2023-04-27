from unittest.mock import MagicMock, patch
from pathlib import Path
import sys
import importlib.util

from autogpt_plugins.unzipped_plugins import AutoGPTAllowUnzippedPlugins


def test_load_unzipped_plugins():
    with patch("autogpt.autogpt.Path.rglob") as rglob_mock, patch(
        "autogpt.autogpt.importlib.util.spec_from_file_location"
    ) as spec_from_file_location_mock, patch(
        "autogpt.autogpt.importlib.util.module_from_spec"
    ) as module_from_spec_mock:
        rglob_mock.return_value = [
            Path("plugins/init.py"),
            Path("plugins/AllowUnzippedPlugins/init.py"),
            Path("plugins/plugin1/init.py"),
        ]

    spec_mock = MagicMock()
    spec_from_file_location_mock.return_value = spec_mock

    loaded_module_mock = MagicMock()
    instance_mock = MagicMock()
    loaded_module_mock.PluginClass.return_value = instance_mock
    module_from_spec_mock.return_value = loaded_module_mock

    plugin_instance = AutoGPTAllowUnzippedPlugins()
    unzipped_plugins = plugin_instance.load_unzipped_plugins()
    assert unzipped_plugins == [instance_mock]

    rglob_mock.assert_called_once_with("__init__.py")
    spec_from_file_location_mock.assert_called_once_with(
        "plugin1", "plugins/plugin1/__init__.py"
    )
    module_from_spec_mock.assert_called_once_with(spec_mock)
    spec_mock.loader.exec_module.assert_called_once_with(loaded_module_mock)
    assert "plugin1" in sys.modules
    loaded_module_mock.PluginClass.assert_called_once_with()
