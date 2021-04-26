# discord libraries
import discord
from discord.ext import tasks, commands
from discord_token import api_token
# stock libraries
import time
import sched
from datetime import date, datetime
import calendar

# to do:
#   - check time and ping loyal_listener when show starts
#       - at sometime like 9 AM every day, checks current weekday
#         and sets timer for every show beginning on that day 
#   - have it ask in #specialty-show-staff an hour before show starts 
#     if show is going to happen
#       - allow announcement to be cancelled if reply is no
#       - or if reply times out
#   - better export function... maybe use pickle?

#client = discord.Client()
client = commands.Bot(command_prefix = '!')

loyal_listener = '<@&830141470345920544>'

class Show(object):
    def __init__(self, name, dj, day, starttime, endtime):
        self.name = name
        self.dj = dj
        self.day = day
        self.starttime = starttime
        self.endtime = endtime

showlist = []

def delete_element(list_object, pos):
    if pos < len(list_object):
        list_object.pop(pos)

@client.event
async def on_ready():
    print(f'Success! Logged in as {client.user}')

#@client.event
#async def on_message(message):
#    # just so the bot doesn't read itself
#    if message.author == client.user:
#        return

class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Colour(0x00ffff), description="")
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

client.help_command = MyHelpCommand()
    
# Add shows
@client.command()
async def addshow(ctx, name=None, dj=None, day=None, starttime=None, endtime=None):
    if not (name == None or endtime == None):
        try:
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="**The Specialty Show has been added.**\n**Show name**: {}\n**DJ name**: DJ {}\n**Day of week**: {}\n**Starting time**: {}\n**Ending time**: {}".format(name, dj, calendar.day_name[int(day)], datetime.strptime(starttime, "%H:%M").strftime("%I:%M %p"), datetime.strptime(endtime, "%H:%M").strftime("%I:%M %p"))))
            newshow = Show(name, dj, day, starttime, endtime)
            showlist.append(newshow)
            return
        except:
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='Invalid input.\nPlease add a show in this format:\n**!addshow "[name]" [DJ name] [day number] [start time] [end time]**\n\nDo not include "DJ" in the DJ name.\n0 = Monday, 1 = Tuesday, 2 = Wednesday, [...], 6 = Sunday\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)'))
            return
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='Invalid input.\nPlease add a show in this format:\n**!addshow "[name]" [DJ name] [day number] [start time] [end time]**\n\nDo not include "DJ" in the DJ name.\n0 = Monday, 1 = Tuesday, 2 = Wednesday, [...], 6 = Sunday\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)'))

# List shows
@client.command()
async def shows(ctx):
    if (len(showlist) <= 0):
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="There are no shows currently loaded!"))
        return
    response = ""
    for i in range(0, len(showlist)):
        appended = "**{}**: **{}** by DJ **{}** on **{}s** from **{}** to **{}**\n".format(i, showlist[i].name, showlist[i].dj, calendar.day_name[int(showlist[i].day)], showlist[i].starttime, showlist[i].endtime)
        response += appended
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description=response))
    
# Remove shows
@client.command()
async def removeshow(ctx, arg=None):
    if not (len(showlist) <= 0 or arg == None):
        try:
            if int(arg) <= len(showlist):
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="Removing {} at indice {}.".format(showlist[int(arg)].name, int(arg))))
                delete_element(showlist, int(arg))
                return
        except:
            pass
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="Invalid input.\nTo remove a show, please type **!removeshow [show number]**\nTo see list of shows and their numbers, please use **!shows**"))

# Backup showlist
@client.command(pass_context=True)
async def backup(ctx):
    # check for shows first
    if len(showlist) == 0:
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="There are no shows currently loaded!"))
        return

    # write to file
    with open("backup.txt", "w") as file:
        showlistf = ""
        showlistf += "Backup generated at: {}\n\n".format(str(datetime.now()))
        for i in showlist:
            showlistf += "Show name: {}\nDJ Name: DJ {}\n{}s from {} to {}\n\n".format(i.name, i.dj, calendar.day_name[int(i.day)], datetime.strptime(i.starttime, "%H:%M").strftime("%I:%M %p"), datetime.strptime(i.endtime, "%H:%M").strftime("%I:%M %p"))
        file.write(showlistf)
    
    # send file to Discord in message
    with open("backup.txt", "rb") as file:
        await ctx.send("Here is the current showlist!", file=discord.File(file, "backup.txt"))

# Import showlist
@client.command(name="import", pass_context=True)
async def importlist(ctx, array=None):
    if (array == None):
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="Function not implemented yet."))
        return

#ping executive staff      
@client.command()
async def ping(ctx):
    await ctx.send(loyal_listener)

@client.command()
async def kill(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Executive Staff")
    if role in ctx.author.roles:
        await ctx.send(f'I have been slain...')
        exit()
    else:
        pass

client.run(api_token)
