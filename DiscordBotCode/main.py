import string
import discord
import os
from dotenv import load_dotenv
from random import choice
from discord.ext import commands
from tr import Trivia

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

async def create_poll(ctx, question, options, reactions):
    description = []
    for x, option in enumerate(options):
        description += '\n {} {} \n'.format(reactions[x], option)
    embed = discord.Embed(title = question, color = 3553599, description = ''.join(description))
    react_message = await ctx.send(embed = embed)
    for reaction in reactions[:len(options)]:
        await react_message.add_reaction(reaction)
    embed.set_footer(text='Poll ID: {}'.format(react_message.id))
    await react_message.edit(embed=embed)

@bot.command(pass_context = True)
async def poll(ctx, poll_type, question, *options: str):
    if poll_type == 'yes no':
        options = ["yes", "no"]
        reactions = ['👍', '👎']
        await create_poll(ctx, question, options, reactions)
    if poll_type == 'voting':
        # if isinstance(options[0], int) == False:
        #     await ctx.send("The second argument should be an integer between 1 and 9")
        #     return
        new_options = []
        for i in range (0, int(options[0])):
            new_options.append(i)
        options = new_options
        reactions = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
        await create_poll(ctx, question, options, reactions)

# once the bot connects, print that it is connected to the command line
@bot.event
async def on_ready():
    print(f'\t{bot.user} has connected to Discord!')


bot.run(TOKEN)