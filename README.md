# ERIS: Discord Bridge

## What is ERIS
This is a simple python program that acts as a bridge between a locally running instance of Ollama and a discord server.  This code is customizable and easily configureable for whatever purpose you need. The name is just a tongue and cheek joke about the greek goddess of discord Eris. Yes I am original.

## Getting started with Discord's api and developer portal
It's important to setup a proper discord bot token. I highly recommend looking at discords documentation for their documentation on their services. https://discord.com/developers/docs/quick-start/getting-started

## Installing the dependancies

Next it's important to install the discord python library, run the following command to install discord.py

```shell
pip install discord.py
```

## Setting up the config file
Updating the bot settings to be an external config file `config.json`

sample of `config.json`

```json
{
    "bot_token": "{Bot_Token}",
    "llama_server_url": "{ollama_server_address}",
    "active_model": "llama3.2:1b",
    "default_model": "llama3.2:1b",
    "model_pre_prompt": "Keep your response short for the user, here is the users message. ",
    "bot_commands": {
        "prompt": "Ask me a question, and I'll respond with an answer.",
        "currentmodel": "Shows current model running.",
        "setmodel": "Allows user to define a differnt model sample `$setmodel llama3.2:1b` will change the model to `llama3.2:1b`.",
        "models": "Lists all installed models on server.",
        "help": "Pretty obvious what this command does."
    },
    "banned_user_list": "",
    "ban_message": "I am sorry, but I cannot assist you at this moment. If you believe is this is a mistake, contact the app owner."
}
```

- `bot_token` the generated bot token form the discord development portal
- `llama_server_url` the locally running ollama instance, if running on a local machine the default address will be `http://localhost:11434`
- `active_model` is the current model set for interacting with discord
- `default_model` is the fall back model if no active model is set or a user inputs an incorrect model name
- `model_pre_prompt` are instructions sent to the llm that set guidelines for the users prompts.
- `bot_commands` general help for the commands that users on discord can query to see what commands they can run.
- `banned_user_list` this can be used to block some users from using the LLM
- `ban_message`  message that displays to the user that they are unable to access the LLM and the reason why

## Response from ollama api

```json
{
    "model": "{Modelname}",
    "created_at": "{TimeStamp}",
    "message": {
        "role": "assistant",
        "content": "Response From LLM"
    },
    "done_reason": "stop",
    "done": true,
    "total_duration": ,
    "load_duration": ,
    "prompt_eval_count": ,
    "prompt_eval_duration": ,
    "eval_count": ,
    "eval_duration": 
}

```

## Limitation
Since discord has a limit of 2000 characters, I highly recommend setting the `model_pre_prompt` to explicitly state that the LLM is suppose to only return short answer and not over explain anything.
