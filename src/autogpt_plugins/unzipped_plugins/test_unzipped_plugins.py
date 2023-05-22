from unittest.mock import MagicMock, Mock, call, patch
from pathlib import Path
import sys
import importlib.util

import os
from . import AutoGPTAllowUnzippedPlugins

import pytest

from .plugin_manager import PluginManager
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


@pytest.fixture
def temp_plugin_folder(tmp_path):
    plugin_dir = tmp_path / "fake_plugins"
    (plugin_dir / "valid_plugin").mkdir(parents=True)
    (plugin_dir / "valid_plugin" / "__init__.py").touch()
    (plugin_dir / "invalid_folder").mkdir(parents=True)
    (plugin_dir / "invalid_folder" / "non_plugin_file.txt").touch()
    return plugin_dir


def test_load_unzipped_plugins_with_non_plugin_files(temp_plugin_folder):
    with patch(
        "importlib.util.spec_from_file_location"
    ) as mock_spec_from_file_location, patch(
        "importlib.util.module_from_spec"
    ) as mock_module_from_spec:
        mock_spec = Mock()
        mock_loaded_module = Mock()
        mock_spec_from_file_location.return_value = mock_spec
        mock_module_from_spec.return_value = mock_loaded_module

        # Test function
        plugins = PluginManager.load_unzipped_plugins(temp_plugin_folder)

        # Check if non-plugin files are ignored
        mock_spec_from_file_location.assert_called_once_with(
            "valid_plugin",
            str((temp_plugin_folder / "valid_plugin" / "__init__.py").resolve()),
        )


@pytest.fixture
def temp_plugin_folder_with_import_error(tmp_path):
    plugin_dir = tmp_path / "fake_plugins_error"
    (plugin_dir / "plugin_with_error").mkdir(parents=True)
    (plugin_dir / "plugin_with_error" / "__init__.py").write_text(
        "import nonexistent_module"
    )
    return plugin_dir


def test_load_unzipped_plugins_with_import_error(temp_plugin_folder_with_import_error):
    with patch(
        "importlib.util.spec_from_file_location"
    ) as mock_spec_from_file_location, patch(
        "importlib.util.module_from_spec"
    ) as mock_module_from_spec:
        mock_spec = Mock()
        mock_spec_from_file_location.return_value = mock_spec

        mock_loaded_module = Mock()
        mock_module_from_spec.return_value = mock_loaded_module
        mock_spec.loader.exec_module.side_effect = ImportError(
            "Failed to import module"
        )

        # Test function
        with pytest.raises(ImportError, match="Failed to import module"):
            PluginManager.load_unzipped_plugins(temp_plugin_folder_with_import_error)


@pytest.fixture
def positive_plugin():
    class PositiveMockPlugin:
        def can_handle_on_response(self):
            return True

        def can_handle_post_prompt(self):
            return True

        def can_handle_post_planning(self):
            return True

        def can_handle_pre_instruction(self):
            return True

        def can_handle_on_instruction(self):
            return True

        def can_handle_post_instruction(self):
            return True

        def can_handle_pre_command(self):
            return True

        def can_handle_post_command(self):
            return True

        def can_handle_user_input(self, user_input: str):
            return True

        def can_handle_report(self):
            return True

    return PositiveMockPlugin()


def test_non_supported_methods(positive_plugin):
    PluginManager = MagicMock()
    PluginManager.load_unzipped_plugins.return_value = [positive_plugin]
    plugin = AutoGPTAllowUnzippedPlugins(plugin_manager=PluginManager)
    plugin._plugins = [positive_plugin]
    assert not plugin.can_handle_on_planning()
    assert not plugin.can_handle_chat_completion(any, any, any, any)
    assert not plugin.can_handle_text_embedding(any)


def test_can_handle_methods_positive(positive_plugin):
    PluginManager = MagicMock()
    PluginManager.load_unzipped_plugins.return_value = [positive_plugin]
    plugin = AutoGPTAllowUnzippedPlugins(plugin_manager=PluginManager)
    plugin._plugins = [positive_plugin]
    assert plugin.can_handle_on_response()
    assert plugin.can_handle_post_prompt()
    assert plugin.can_handle_post_planning()
    assert plugin.can_handle_pre_instruction()
    assert plugin.can_handle_on_instruction()
    assert plugin.can_handle_post_instruction()
    assert plugin.can_handle_pre_command()
    assert plugin.can_handle_post_command()
    assert plugin.can_handle_user_input("test")
    assert plugin.can_handle_report()


@pytest.fixture
def negative_plugin():
    class NegativeMockPlugin:
        def can_handle_on_response(self):
            return False

        def can_handle_post_prompt(self):
            return False

        def can_handle_post_planning(self):
            return False

        def can_handle_pre_instruction(self):
            return False

        def can_handle_on_instruction(self):
            return False

        def can_handle_post_instruction(self):
            return False

        def can_handle_pre_command(self):
            return False

        def can_handle_post_command(self):
            return False

        def can_handle_user_input(self, user_input: str):
            return False

        def can_handle_report(self):
            return False

    return NegativeMockPlugin()


def test_can_handle_methods_negative(negative_plugin):
    PluginManager = MagicMock()
    PluginManager.load_unzipped_plugins.return_value = [negative_plugin]
    plugin = AutoGPTAllowUnzippedPlugins(plugin_manager=PluginManager)
    plugin._plugins = [negative_plugin]
    assert not plugin.can_handle_on_response()
    assert not plugin.can_handle_post_prompt()
    assert not plugin.can_handle_post_planning()
    assert not plugin.can_handle_pre_instruction()
    assert not plugin.can_handle_on_instruction()
    assert not plugin.can_handle_post_instruction()
    assert not plugin.can_handle_pre_command()
    assert not plugin.can_handle_post_command()
    assert not plugin.can_handle_user_input("test")
    assert not plugin.can_handle_report()


@pytest.fixture(scope="function")
def plugin_mock_onhandle():
    plugin_A = MagicMock()
    plugin_A.can_handle_on_response.return_value = True
    plugin_A.on_response.side_effect = lambda response, *args, **kwargs: response + "A"

    plugin_B = MagicMock()
    plugin_B.can_handle_on_response.return_value = True
    plugin_B.on_response.side_effect = lambda response, *args, **kwargs: response + "B"

    PluginManager = MagicMock()
    PluginManager.load_unzipped_plugins.return_value = [plugin_A, plugin_B]
    plugin = AutoGPTAllowUnzippedPlugins(plugin_manager=PluginManager)
    plugin._plugins = [plugin_A, plugin_B]
    return plugin


def test_handle_on_response(plugin_mock_onhandle):
    response = plugin_mock_onhandle.on_response("Test response")
    assert response == "Test responseAB"


def test_handle_post_prompt(plugin_mock_onhandle):
    prompt = "Test prompt"
    for plugin in plugin_mock_onhandle._plugins:
        plugin.can_handle_post_prompt.return_value = True
        plugin.post_prompt.side_effect = lambda prompt: prompt + " modified"
    new_prompt = plugin_mock_onhandle.post_prompt(prompt)
    assert new_prompt == "Test prompt modified modified"


def test_handle_post_planning(plugin_mock_onhandle):
    response = "Test response"
    for plugin in plugin_mock_onhandle._plugins:
        plugin.can_handle_post_planning.return_value = True
        plugin.post_planning.side_effect = lambda response: response + " modified"
    new_response = plugin_mock_onhandle.post_planning(response)
    assert new_response == "Test response modified modified"


def test_handle_pre_instruction(plugin_mock_onhandle):
    messages_list = [{"role": "user", "content": "Hi"}]

    plugin_A = plugin_mock_onhandle._plugins[0]
    plugin_A.can_handle_pre_instruction.return_value = True
    plugin_A.pre_instruction.side_effect = lambda msgs: [
        {"role": "plugin_a", "content": "Plugin A message"}
    ]

    plugin_B = plugin_mock_onhandle._plugins[1]
    plugin_B.can_handle_pre_instruction.return_value = True
    plugin_B.pre_instruction.side_effect = lambda msgs: [
        {"role": "plugin_b", "content": "Plugin B message"}
    ]

    result_messages = plugin_mock_onhandle.pre_instruction(messages_list)
    assert len(result_messages) == 3
    assert result_messages[1]["role"] == "plugin_a"
    assert result_messages[2]["role"] == "plugin_b"


def test_handle_on_instruction(plugin_mock_onhandle):
    messages_list = [{"role": "user", "content": "Hi"}]

    plugin_A = plugin_mock_onhandle._plugins[0]
    plugin_A.can_handle_on_instruction.return_value = True
    plugin_A.on_instruction.side_effect = lambda msgs: "Plugin A result"

    plugin_B = plugin_mock_onhandle._plugins[1]
    plugin_B.can_handle_on_instruction.return_value = True
    plugin_B.on_instruction.side_effect = lambda msgs: "Plugin B result"

    result = plugin_mock_onhandle.on_instruction(messages_list)
    assert result == "Plugin A result\nPlugin B result"


def test_handle_post_instruction(plugin_mock_onhandle):
    instructions = [{"role": "instructor", "content": "Instruction"}]

    plugin_A = plugin_mock_onhandle._plugins[0]
    plugin_A.can_handle_post_instruction.return_value = True
    plugin_A.post_instruction.side_effect = lambda instructions: instructions + [
        {"role": "plugin_a", "content": "Plugin A post instruction"}
    ]

    plugin_B = plugin_mock_onhandle._plugins[1]
    plugin_B.can_handle_post_instruction.return_value = True
    plugin_B.post_instruction.side_effect = lambda instructions: instructions + [
        {"role": "plugin_b", "content": "Plugin B post instruction"}
    ]

    result_instructions = plugin_mock_onhandle.post_instruction(instructions)
    assert len(result_instructions) == 3
    assert result_instructions[1]["role"] == "plugin_a"
    assert result_instructions[2]["role"] == "plugin_b"
