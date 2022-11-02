import string
import discord
import os
from dotenv import load_dotenv
from random import choice
from discord.ext import commands
from tr import Trivia
from help import Trivia as trivia_help
from help import Poll as poll_help
from help import NineNine as ninenine_help
from help import Happy as happy_help

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
    if options:
        for x, option in enumerate(options):
            description += '\n {} {} \n'.format(reactions[x], option)
    embed = discord.Embed(title = question, color = 3553599, description = ''.join(description))
    react_message = await ctx.send(embed = embed)
    if not options:
        for reaction in reactions:
            await react_message.add_reaction(reaction)
    elif options:
        for reaction in reactions[:len(options)]:
            await react_message.add_reaction(reaction)
    embed.set_footer(text='Poll ID: {}'.format(react_message.id))
    await react_message.edit(embed=embed)

@bot.command(pass_context = True)
async def poll(ctx, poll_type, question = "help", *options: str):
    if poll_type == 'yes no':
        if question == "help":
            await ctx.send("To create a yes/no poll, use the command:\n\
                !poll 'yes no' '<question>'")
            return
        options = ["yes", "no"]
        reactions = ['👍', '👎']
        await create_poll(ctx, question, options, reactions)
    if poll_type == 'voting':
        if question == "help":
            await ctx.send("To create a voting poll, use the command:\n\
                !poll voting '<option 1>' '<option 2>' ... '<option 10>'\n\n\
                You may use anywhere from 1 to 10 options.")
            return
        new_options = []
        for i in range (0, len(options)):
            new_options.append(options[i])
        options = new_options
        reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
        await create_poll(ctx, question, options, reactions)
    if poll_type == 'rating':
        options = None
        reactions = ['😆', '😁', '😀', '🙂', '😐', '😕', '🙁', '😔', '😣', '😫']
        await create_poll(ctx, question, options, reactions)
    if poll_type == "help":
        await ctx.send("The poll command is as follows:\n\
            !poll '<poll type>' '<poll arguments>'\n\n\
        The possible poll types are:\n\
            - 'yes no': for a thumbs up or thumbs down poll\n\
            - 'voting': for a 1-10 option poll")

@bot.command(name="trivia")
async def trivia(ctx, category="none", difficulty="none"):
    #user = ctx.author
    responses = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
    triviaQuestion = Trivia(category, difficulty)
    questionList = triviaQuestion.formatQuestion()
    printMsg = ""
    for i in range(len(questionList)):
        printMsg += questionList[i] + '\n'
    triviaMsg = await ctx.send(printMsg)
    message = await ctx.channel.send(triviaMsg)
    for j in range(triviaQuestion.getQuestionCount()):
        await message.add_reaction(responses[j])

# once the bot connects, print that it is connected to the command line
@bot.event
async def on_ready():
    print(f'\t{bot.user} has connected to Discord!')


bot.run(TOKEN)