import datetime
import discord
from discord.ext import commands
import json
import logging
import requests
import os
import sys

# Read from config file
def read_config(file_path):
    with open(file_path, 'r') as f:
        config_data = json.load(f)
    return config_data

# Write to config file
def write_config(file_path, config_data):
    with open(file_path, 'w') as f:
        json.dump(config_data, f, indent=4)

# Init Discord Bot Configs
intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# Init Config
config = read_config("config.json")
BOT_TOKEN = config["bot_token"]
ollama_url = config["llama_server_url"]
active_model = config["active_model"]
default_model = config["default_model"]
pre_prompt = config["model_pre_prompt"]
ban_list = config["banned_user_list"]
ban_message = config["ban_message"]


# Init static values
ollama_API = ollama_url+"/api/chat"
modelList_API = ollama_url+"/api/tags"
headers = {"Content-Type": "application/json"}


def ai_gen(prompt):
    data = {
        "model": config["active_model"],
        "messages": [
            {
            "role": "user",
            "content": pre_prompt + "'" + prompt + "'"
            }
        ],
        "stream": False
    }

    # Make POST request to Ollama API
    response = requests.post(ollama_API, headers=headers, data=json.dumps(data))
    response_json = response.json()
    model_message = response_json["message"]["content"]

    if response.status_code == 200:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Success request back ollama. Status Code: ", response.status_code)
        return model_message
    else:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Failed to send request. Status code: ", response.status_code)
        return None

def setModel(model):
    if model is None:
        active_model = "llama3.2:1b"

    config['active_model'] = model.strip()
    write_config("config.json", config)
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Success model change. New Model: ", model.strip())
    return "`Active Model: " + model + "`"

def currentModel():
    return "`Current Model: " + active_model + "`"

def listModels():
    list = "Here are the current models I have: \n"
    response = requests.get(modelList_API)
    response_json = response.json()
    for item in response_json["models"]:
        list += "`" + item["model"] + "`    family: " + item["details"]["family"] + "    parameter: " + item["details"]["parameter_size"] + "\n"

    if response.status_code == 200:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Success request back ollama. Status Code: ", response.status_code)
        return list
    else:
        print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " Failed to send request. Status code: ", response.status_code)
        return None

    if queue == question_limit:
        return ai_response

def bot_commands():
    with open("config.json", 'r') as f:
        commands = "List of current bot commands: \n"
        data = json.load(f)
        for key, value in data["bot_commands"].items():
            commands += "`$" + key +"`     "+ value + "\n"
        return commands

@client.event
async def on_ready():
    active_model = config["active_model"]
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    username: str = str(message.author)
    userid: str = str(message.author.id)
    user_message: str = message.content
    channel: str = str(message.channel)

    if message.content.startswith('$help'):
        await message.channel.send(bot_commands())

    if message.content.startswith('$prompt'):
        if userid in ban_list:
            await message.channel.send(ban_message)
        else:
            userMessage = message.content.replace('$prompt', '')
            await message.channel.send(ai_gen(userMessage))

    if message.content.startswith('$setmodel'):
       model = message.content.replace('$setmodel', '')
       await message.channel.send(setModel(model))
       os.execv(sys.executable, ['python'] + sys.argv)

    if message.content.startswith('$currentmodel'):
        model = message.content.replace('$currentmodel', '')
        await message.channel.send(currentModel())

    if message.content.startswith('$models'):
        await message.channel.send(listModels())


client.run(BOT_TOKEN)


