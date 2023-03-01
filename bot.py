import os
import json
import discord

from datetime import datetime
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

def mocker(sentence):
    new_sentence = []
    for index,letter in enumerate(sentence):
        if index%2==0:
            new_sentence.append(letter.upper())
        else:
            new_sentence.append(letter.lower())
    return ''.join(new_sentence)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

idiots_who_asked_for_help = {"Newk":datetime.now()}
@client.event
async def on_message(message):
    if message.author == client.user:
        return


    if idiots_who_asked_for_help.get(message.author.nick) is not None:
        
        # check if the idiot tried to ask for help in the last 5 minutes
        if idiots_who_asked_for_help[message.author.nick] < datetime.now() + datetime.timedelta(minutes=5):
            
            # if so, mock them ruthlessly 
            return_message = message.content + f"\n i'm {message.author.nick} and i couldnt figure out how to use the bot"
            message.channel.send(mocker(return_message))
    
    if message.content[:5] == "!help":
        # be mean, for no reason
        idiots_who_asked_for_help[message.author.nick] = datetime.now()
        await message.channel.send("shut the fuck up, idiot")


    if message.content[:5] == "!chat":
        print(f"running prompt: {message.content[6:]}")
        for data in chatbot.ask(message.content[6:]):            
            response = data["message"]
            print(response)

        for sub_message in response.split("\n"):
            for message_chunk in chunkstring(sub_message, length=1999):
                await message.channel.send(message_chunk)



client.run(TOKEN)