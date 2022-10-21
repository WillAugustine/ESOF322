import discord
import os
from dotenv import load_dotenv
from random import randint

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        'Cool. Cool cool cool cool cool cool cool,',
        'no doubt no doubt no doubt no doubt.'
    ]

    if '99' in message.content.lower():
        response = brooklyn_99_quotes[randint(0,3)]
        await message.channel.send(response)
        
    elif 'happy birthday' in message.content.lower():
        await message.channel.send('Happy Birthday! 🎈🎉')


client.run(TOKEN)