import string
import discord
import os
from dotenv import load_dotenv
from random import choice
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

# prefix for messages intended for the bot
bot = commands.Bot(intents=discord.Intents.all(), command_prefix='!')


brooklyn_99_quotes = [
    'I\'m the human form of the 💯 emoji.',
    'Bingpot!',
    'Cool. Cool cool cool cool cool cool cool,',
    'no doubt no doubt no doubt no doubt.'
]

# when '!99' command is used, print Brooklyn 99 quote from array definied above
@bot.command(name="99", help='Responds with a random quote from Brooklyn 99')
async def nine_nine(ctx):
    response = choice(brooklyn_99_quotes)
    await ctx.send(response)

# takes input after '!happy' command and spits it out in celebratory message
@bot.command(name="happy", help='Responds with a celebratory message')
async def happy_birthday(ctx,*,message):
    await ctx.send(f'Happy {message}! 🎈🎉')

# once the bot connects, print that it is connected to the command line
@bot.event
async def on_ready():
    print(f'\t{bot.user} has connected to Discord!')

bot.run(TOKEN)