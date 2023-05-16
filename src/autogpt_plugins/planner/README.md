# AutoGPT Planner Plugin
Simple planning commands for planning leveraged with chatgpt3.5 and json objects to keep track of its progress on a list of tasks.

![image](https://user-images.githubusercontent.com/12145726/235688701-af549b76-7f9f-4426-9c88-dd72aca45685.png)


### Getting started

After you clone the plugin from the original repo (https://github.com/rihp/autogpt-planner-plugin) Add it to the plugins folder of your AutoGPT repo and then run AutoGPT

![image](https://user-images.githubusercontent.com/12145726/235688224-7abf6ae4-5c0a-4e2d-b1b2-18241c6d74b4.png)

Remember to also update your .env to include 

```
ALLOWLISTED_PLUGINS=PlannerPlugin
```



# New commands
```python
prompt.add_command(
    "check_plan",
    "Read the plan.md with the next goals to achieve",
    {},
    check_plan,
)

prompt.add_command(
    "run_planning_cycle",
    "Improves the current plan.md and updates it with progress",
    {},
    update_plan,
)

prompt.add_command(
    "create_task",
    "creates a task with a task id, description and a completed status of False ",
    {
        "task_id": "<int>",
        "task_description": "<The task that must be performed>",
    },
    create_task,
)

prompt.add_command(
    "load_tasks",
    "Checks out the task ids, their descriptionsand a completed status",
    {},
    load_tasks,
)

prompt.add_command(
    "mark_task_completed",
    "Updates the status of a task and marks it as completed",
    {"task_id": "<int>"},
    update_task_status,
)
```

# New config options
By default, the plugin is set ot use what ever your `FAST_LLM_MODEL` environment variable is set to, if none is set it 
will fall back to `gpt-3.5-turbo`. If you want to set it individually to a different model you can do that by setting
the environment variable `PLANNER_MODEL` to the model you want to use (example: `gpt-4`).

Similarly, the token limit defaults to the `FAST_TOKEN_LIMIT` environment variable, if none is set it will fall 
back to `1500`. If you want to set it individually to a different limit for the plugin you can do that by setting
`PLANNER_TOKEN_LIMIT` to the desired limit (example: `7500`).

And last, but not least, the temperature used defaults to the `TEMPERATURE` environment variable, if none is set it will 
fall back to `0.5`. If you want to set it individually to a different temperature for the plugin you can do that by 
setting `PLANNER_TEMPERATURE` to the desired temperature (example: `0.3`).


## CODE SAMPLES

Example of generating an improved plan
```python
def generate_improved_plan(prompt: str) -> str:
    """Generate an improved plan using OpenAI's ChatCompletion functionality"""

    import openai

    tasks = load_tasks()

    # Call the OpenAI API for chat completion
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that improves and adds crucial points to plans in .md format.",
            },
            {
                "role": "user",
                "content": f"Update the following plan given the task status below, keep the .md format:\n{prompt}\nInclude the current tasks in the improved plan, keep mind of their status and track them with a checklist:\n{tasks}\Revised version should comply with the contests of the tasks at hand:",
            },
        ],
        max_tokens=1500,
        n=1,
        temperature=0.5,
    )
```


## Testing workflow

Clone the repo and modify the functionality, when you're done you can run 
```
zip -ru ../fork/plugins/planner.zip . ; cd ../fork && python3 -m autogpt --debug 
```

then you need to cd back to 
```
cd ../autogpt-planner-plugin    
```
