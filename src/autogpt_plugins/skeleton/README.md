# AutoGPT Skeleton Plugin
This plugin is based on the AutoGPT Planner Plugin

## Getting Started

After you clone this repo from the original repo add it to the plugins folder of your AutoGPT repo and then run AutoGPT.

Remember to also update your `.env` to include

    ALLOWLISTED_PLUGINS=SkeletonPlugin
    SKELETON_MODEL=gpt-4
    SKELETON_TOKEN_LIMIT=7500
    SKELETON_TEMPERATURE=0.3

## New Commands

This plugin adds many new commands, here's the list:

```python
        prompt.add_command(
            "list_code_structure",
            "List the current code structure",
            {},
            list_code_structure,
        )

        prompt.add_command(
            "update_code_structure",
            "Update the code structure with descriptions of new files",
            {},
            update_code_structure,
        )

        prompt.add_command(
            "force_update_code_structure",
            "Force update the code structure with new descriptions for all files",
            {},
            force_update_code_structure,
        )

        prompt.add_command(
            "create_file",
            "Creates a new file with a given name and optional initial content",
            {
                "file_name": "<string>",
                "initial_content": "<optional string>",
            },
            create_file,
        )

        prompt.add_command(
            "write_to_file",
            "Writes to a specified file",
            {
                "file_name": "<string>",
                "content": "<string>",
            },
            write_to_file,
        )

        prompt.add_command(
            "create_directory",
            "Creates a new directory",
            {
                "directory_name": "<string>",
            },
            create_directory,
        )

        prompt.add_command(
            "change_directory",
            "Changes the current directory",
            {
                "directory_name": "<string>",
            },
            change_directory,
        )

        prompt.add_command(
            "list_files",
            "Lists all the files in the current directory",
            {},
            list_files,
        )

```

## New Config Options

By default, the plugin uses whatever your `FAST_LLM_MODEL` environment variable is set to. If none is set it will fall back to `gpt-3.5-turbo`. You can set it individually to a different model by setting the environment variable `SKELETON_MODEL` to the model you want to use (example: `gpt-4`).

Similarly, the token limit defaults to the `FAST_TOKEN_LIMIT` environment variable. If none is set it will fall back to `1500`. You can set it individually to a different limit for the plugin by setting `SKELETON_TOKEN_LIMIT` to the desired limit (example: `7500`).

The temperature used defaults to the `TEMPERATURE` environment variable. If none is set it will fall back to `0.5`. You can set it individually to a different temperature for the plugin by setting `SKELETON_TEMPERATURE` to the desired temperature (example: `0.3`).
