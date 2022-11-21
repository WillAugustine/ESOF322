import string
import discord
import os
from dotenv import load_dotenv
from random import choice
from discord.ext import commands
from tr import Trivia
import youtube_dl as YT
from discord.channel import VoiceChannel

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
@bot.command(name="happy",help='Responds with a celebratory message')
async def happy_birthday(ctx,*,message:str = commands.parameter(description="The thing you are celebrating")):
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
@bot.command(help="Generates a trivia question. Type \'!trivia categories\' for all trivia categories n' stuff.")
#async def happy_birthday(ctx,*,message:str = commands.parameter(description="The thing you are celebrating")):
async def trivia(ctx, 
    category:str=commands.parameter(default="none", description="The category of trivia question you want to answer"),
    difficulty:str=commands.parameter(description="The difficulty of the question. Either easy, medium, or hard", default="none")):
    if category == "categories":
        tr = Trivia()
        printMsg = ""
        for i in tr.showCategories():
            printMsg += i + '\n'
        await ctx.send(printMsg)
    else:
        user = ctx.author
        chnl = ctx.channel
        triviaQuestion = Trivia(category, difficulty)
        questionList = triviaQuestion.formatQuestion()
        printMsg = ""
        for i in questionList:
            printMsg += i + '\n'
        triviaMsg = await ctx.send(printMsg)
        userResponse = await bot.wait_for('message')
        while (userResponse.author != user or userResponse.channel != chnl):
            userResponse = await bot.wait_for('message')
            try:
                n = int(userResponse)
            except:
                userResponse = None
        await ctx.send(f"**{ctx.author}**, you responded with {userResponse.content}!")
        answeredCorrectly = triviaQuestion.checkAnswer(int(userResponse.content))
        await ctx.send(str(answeredCorrectly))
        if (not answeredCorrectly):
            await ctx.send("The correct answer was " + triviaQuestion.returnAnswer())
    

YT.utils.bug_reports_message = lambda: ''
TY_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = YT.YoutubeDL(TY_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

async def join(ctx, desired_channel):

    target_channel = discord.utils.get(ctx.guild.channels, name=desired_channel)
    channel_id = target_channel.id
    channel = bot.get_channel(channel_id)
    print(f"\tLooking for channel '{channel.name}' of type '{channel.type}'")
    
    
    if ctx.voice_client:
        await ctx.voice_state.voice.move_to(channel)
        return
    await channel.connect()
    #await ctx.send(f"The bot joined the voice channel {channel.name}")

async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_connected():
        await voice_client.disconnect()
    else:
        await ctx.send("The bot is not connected to a voice channel.")

@bot.group(pass_context = True, help="Plays music in the channel you are in")
async def music(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid poll command passed')

def formatYoutubeVideo(filename):
    output = [filename[0], ""]
    used_dash = False
    first_string = True
    for i in range(1, len(filename)):
        if filename[i].isupper() and not used_dash:
            output[0] = output[0] + filename[i]
        elif filename[i] == '-':
            if not used_dash:
                used_dash = True
            else:
                return output
        elif filename[i] == '_':
            if used_dash:
                output[1] = output[1] + " "
            else:
                output[0] = output[0] + " "
        else:
            if used_dash:
                output[1] = output[1] + filename[i]
            else:
                output[0] = output[0] + filename[i]
    return output

    
@music.command(name='play_song', help='This command plays the song')
async def play(ctx,
    url: str = commands.parameter(description="The YouTube URL you want to play"),
    channel: str = commands.parameter(description="The channel you want to play music in")):
    await join(ctx, channel)
    try :
        server = ctx.message.guild
        voice_channel = server.voice_client
        async with ctx.typing():
            filename = await YTDLSource.from_url(url, loop=bot.loop)
            voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
        formattedFilename = formatYoutubeVideo(filename)
        title = formattedFilename[1]
        title = title[1:]
        artist = formattedFilename[0]
        artist = artist[:-1]
        await ctx.send('**Now playing:** *{}* by {} in the *{}* channel'.format(title, artist, channel))
    except Exception as e:
        print(str(e))
        await ctx.send("The bot is not connected to a voice channel.")


@music.command(name='pause', help='This command pauses the currently playing song')
async def pause(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.pause()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    
@music.command(name='resume', help='This command resumes the currently paused song')
async def resume(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_paused():
        voice_client.resume()
    else:
        await ctx.send("The bot was not playing anything before this. Use play_song command")

@music.command(name='stop', help='The command stops the song and the bot leaves the audio channel')
async def stop(ctx):
    voice_client = ctx.message.guild.voice_client
    if voice_client.is_playing():
        voice_client.stop()
    else:
        await ctx.send("The bot is not playing anything at the moment.")
    await leave(ctx)
    
# once the bot connects, print that it is connected to the command line
@bot.event
async def on_ready():
    print(f'\t{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game("!help"))

bot.run(TOKEN)