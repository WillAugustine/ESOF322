import string
import discord
import os
from dotenv import load_dotenv
from random import choice
from discord.ext import commands
from tr import Trivia
# from help import Trivia as trivia_help
# from help import Poll as poll_help
# from help import NineNine as ninenine_help
# from help import Happy as happy_help

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

@bot.group(pass_context = True, help="Creates a poll of the selected type")
async def poll(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid poll command passed')

@poll.command(help="Creates a poll with thumbs up and thumbs down as reactions")
async def yesno(ctx,
    question: str = commands.parameter(description="The yes/no question you want to be answered")):
    options = ["yes", "no"]
    reactions = ['👍', '👎']
    await create_poll(ctx, question, options, reactions)

@poll.group(help="Creates a poll with numbers 1-10 as reactions")
async def voting(ctx,
    question:str = commands.parameter(description="The poll title"),
    *options:str):# = commands.parameter(description="The different options, sepereated by a spcae, for users to vote on (up to 10)")):
    new_options = []
    for i in range (0, len(options)):
        new_options.append(options[i])
    options = new_options
    reactions = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
    await create_poll(ctx, question, options, reactions)

@voting.command(help="The different options, sepereated by a space, for users to vote on (up to 10)")
async def options(ctx):
    pass

@poll.command(help="Creates a poll with 10 different emoji emotions as reactions")
async def rating(ctx,
    question: str = commands.parameter(description="The question you want people to react to")):
    options = None
    reactions = ['😆', '😁', '😀', '🙂', '😐', '😕', '🙁', '😔', '😣', '😫']
    await create_poll(ctx, question, options, reactions)
    
#Trivia Command
@bot.command(name="trivia", help="Generates a trivia question.")
async def trivia(ctx, category="none", difficulty="none"):
    user = ctx.author
    responses = ['1️⃣', '2️⃣', '3️⃣', '4️⃣']
    triviaQuestion = Trivia(category, difficulty)
    questionList = triviaQuestion.formatQuestion()
    printMsg = ""
    for i in range(triviaQuestion.getQuestionCount()):
        printMsg += questionList[i] + '\n'
    triviaMsg = await ctx.send(printMsg)
    for j in range(len(responses)):
        await triviaMsg.add_reaction(responses[j])
    userResponse = await on_reaction_add(triviaMsg.reactions, user)
    answeredCorrectly = triviaQuestion.checkAnswer(userResponse)
    await ctx.send(str(answeredCorrectly))

@bot.event
async def on_reaction_add(reaction, user):
    emo = reaction.emoji
    if emo == '1️⃣':
        return 1
    elif emo == '2️⃣':
        return 2
    elif emo == '3️⃣':
        return 3
    elif emo == '4️⃣':
        return 4

# once the bot connects, print that it is connected to the command line
@bot.event
async def on_ready():
    print(f'\t{bot.user} has connected to Discord!')


bot.run(TOKEN)