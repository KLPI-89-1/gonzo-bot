import discord
from discord.ext import commands
from discord_token import api_token

#client = discord.Client()
client = commands.Bot(command_prefix = '!')

class Show(object):
    def __init__(self, name, dj, day, starttime, endtime):
        self.name = name
        self.dj = dj
        self.day = day
        self.starttime = starttime
        self.endtime = endtime

shows = []

def delete_element(list_object, pos):
    if pos < len(list_object):
        list_object.pop(pos)

@client.event
async def on_ready():
    print('Success! Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    # just so the bot doesn't read itself
    if message.author == client.user:
        return
    
    # Add shows
    if message.content.startswith('!bot addshow'):
        if (message.content == '!bot addshow'):
            await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="Invalid input.\nPlease add a show in this format:\n!bot addshow [name], [DJ name], [day of week], [start time], [end time]"))
        else:
            arg = message.content.replace('!bot addshow ', '').split(', ')
            if len(arg) != 5:
                await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="Invalid input.\nPlease add a show in this format:\n!bot addshow [name], [DJ name], [day of week], [start time], [end time]"))
            else:
                await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="**The Specialty Show has been added.**\n__Show name__: {}\n__DJ name__: {}\n__Day of week__: {}\n__Starting time__: {}\n__Ending time__: {}".format(arg[0], arg[1], arg[2], arg[3], arg[4])))
                newshow = Show(arg[0], arg[1], arg[2], arg[3], arg[4])
                shows.append(newshow)
    
    # List shows
    if message.content.startswith("!bot shows"):
        if (len(shows) <= 0):
            await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="There are no shows currently loaded!"))
            return
        response = ""
        for i in range(0, len(shows)):
            appended = "**{}**: **{}** by **{}** from **{}** - **{}**\n".format(i, shows[i].name, shows[i].dj, shows[i].starttime, shows[i].endtime)
            response += appended
        await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description=response))
    
    # Remove shows
    if message.content.startswith("!bot removeshow"):
        if (len(shows) <= 0):
            await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="There are no shows currently loaded!"))
            return
        if (message.content == '!bot removeshow'):
            await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="Invalid input.\nTo remove a show, please type **!bot removeshow [show number]**\nTo see list of shows and their numbers, please use **!bot shows**"))
            return
        number = message.content.replace("!bot removeshow ", "").split(" ")
        if int(number[0]) <= len(shows):
            await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="Removing {} at indice {}.".format(shows[int(number[0])].name, int(number[0]))))
            delete_element(shows, int(number[0]))

    @client.command()
    async def kill(ctx):
        role = discord.utils.get(ctx.guild.roles, name="Executive Staff")
        if role in ctx.author.roles:
            await ctx.send(f'I have been slain...')
            exit()
        else:
            await ctx.send(f"Not exec staff!!")
    
    # test
    if message.content.startswith("!bot ping"):
        await message.channel.send("@Executive Staff")

client.run(api_token)
