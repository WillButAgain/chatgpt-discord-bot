import os
import json
import discord
from dotenv import load_dotenv

from revChatGPT.V1 import Chatbot


load_dotenv()
with open('config.json', "r") as file:
    data = json.load(file)
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

chatbot = Chatbot(config={
  "email": data["email"],
  "password": data["password"]
})

client = discord.Client(intents=discord.Intents.all())

def chunkstring(string, length):
    return [string[0+i:length+i] for i in range(0, len(string), length)]

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content[:5] == "!chat":
        print(f"running prompt: {message.content[6:]}")
        for data in chatbot.ask(message.content[6:]):            
            response = data["message"]
            print(response)

        for sub_message in response.split("\n"):
            for message_chunk in chunkstring(sub_message, length=1999):
                await message.channel.send(message_chunk)



client.run(TOKEN)