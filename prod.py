# stock libraries
import time
from random import randint
import sched
from datetime import date, datetime
import calendar

# discord libraries
import discord
from discord.ext import tasks, commands
from discord_token import api_token

# to do:
#   - have it ask in #specialty-show-staff an hour before show starts 
#     if show is going to happen
#       - allow announcement to be cancelled if reply is no
#       - or if reply times out
#   - better export function... maybe use pickle?

#client = discord.Client()
client = commands.Bot(command_prefix = '!klpi ')

loyal_listener = '<@&830141470345920544>'
alerts_channel = 830121001450471475

DEBUG = False

# lol just gonna slap this here so i can use it
def delete_element(list_object, pos):
    if pos < len(list_object):
        list_object.pop(pos)

class Show(object):
    def __init__(self, name, dj, day, starttime, endtime):
        self.name = name
        self.dj = dj
        self.day = day
        self.starttime = starttime
        self.endtime = endtime

showlist = []

@client.event
async def on_ready():
    print(f'Success! Logged in as {client.user}')
    # now we're gonna sleep until we're on the hour!
    # why? because im lazy and this is an easy way to calibrate the bot
    checker.start()

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

# About
@client.command()
async def about(ctx):
    random_quotes = ["I am bad at my job... I'm sorry. :(",
    "Nice to meet you too... ;)",
    "Where have all the merry exec staff gone?",
    "I still believe in Pickle Nick.",
    "Annie isn't actually as evil as you think.\nShe's **much** worse.",
    "Mucinex in. Mucus out. Or so I've been told...",
    "I'm trying my best... ;-;",
    "YO WHEN'S THE BOT GONNA BE DONE?????",
    "Have you visited klpi.latech.edu recently?",
    "This is KLPI 89.1, RRRRRRRRUSTON'S ROCK ALTERNATIVE."]
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="**KLPI Specialty Shows Bot v0.1**\nWritten by Josh I. (jpegjpeg#6844)\nThis bot was built using Discord.py\n\n{}".format(random_quotes[randint(0, len(random_quotes)-1)])))


##########################################

# main loop
@tasks.loop(minutes=1.0)
async def checker():
    if len(showlist) >= 1:
        if DEBUG == True:
            print("Checking showlists now...")
        for i in showlist:
            if i.day == calendar.day_name[datetime.now().weekday()]:
                if int(datetime.strptime(i.starttime, "%H:%M").strftime("%H:%M")[0:2]) == datetime.now().hour:
                    if datetime.now().minute == 0:
                        channel = client.get_channel(alerts_channel)
                        await channel.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description=ping_loyal(i)))
                        break
    else:
        if DEBUG == True:
            print("Tried to enter loop, but showlist is empty... waiting for one minute")

def ping_loyal(show):
    random_message = [
        "What's rockin', Ruston?",
        "You hear that?",
        "Something's a-rumblin' at KLPI...",
        "What's that noise?"
        "I can hear it coming in the air tonight...",
        "It's time.",
        "Guess what?",
        "You guessed correctly!",
        "Live and in the flesh! Or... on the airwaves..."
    ]
    return "{}\n**DJ {}** is live with **{}**!\nTune in online or at 89.1 FM! {}".format(random_message[randint(0, len(random_message)-1)], show.dj, show.name, loyal_listener)

##########################################

@checker.before_loop
async def before_checker():
    while (datetime.now().second != 0 and DEBUG == False):
        print(f"Current time: {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}... Need to be on the minute... Calibrating... (sleeping for 1 second)")
        time.sleep(1)
    print(f"\n\nIt is on the hour! Hello world!")

##########################################

# Add shows
@client.command()
async def addshow(ctx, name=None, dj=None, day=None, starttime=None, endtime=None):
    if (name != None and endtime != None):
        try:
            # im lazy and this is the easiest way to sanitize it and fix lowercase entries
            for i in range(-2, 8):
                if day.lower() == calendar.day_name[i].lower() and starttime >= "01:00" and endtime <= "23:59":
                    newshow = Show(name, dj, calendar.day_name[i], starttime, endtime)
                    showlist.append(newshow)
                    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="**The Specialty Show has been added.**\n\n**Show name**: {}\n**DJ name**: DJ {}\n**Day of week**: {}\n**Starting time**: {}\n**Ending time**: {}".format(name, dj, calendar.day_name[i], datetime.strptime(starttime, "%H:%M").strftime("%I:%M %p"), datetime.strptime(endtime, "%H:%M").strftime("%I:%M %p"))))
                    break
            return
        except:
            if DEBUG == True:
                print(f"!addshow tried and failed!\tShow name: {name} DJ: {dj} Day: {day} From: {starttime}-{endtime}")
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='Invalid input.\nPlease add a show in this format:\n**!addshow "[name]" [DJ name] [weekday] [start time] [end time]**\n\nDo not include "DJ" in the DJ name.\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)'))
            return
    if DEBUG == True:
        print(f"!addshow failed! Garbage input provided!\tShow name: {name} DJ: {dj} Day: {day} From: {starttime}-{endtime}")
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='Invalid input.\nPlease add a show in this format:\n**!addshow "[name]" [DJ name] [weekday] [start time] [end time]**\n\nDo not include "DJ" in the DJ name.\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)'))

# List shows
@client.command()
async def shows(ctx):
    if (len(showlist) <= 0):
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="There are no shows currently loaded!"))
        return
    response = ""
    for i in range(0, len(showlist)):
        appended = "**{}**: **{}** by DJ **{}** on **{}s** from **{}** to **{}**\n".format(i, showlist[i].name, showlist[i].dj, showlist[i].day, datetime.strptime(showlist[i].starttime, "%H:%M").strftime("%I:%M %p"), datetime.strptime(showlist[i].endtime, "%H:%M").strftime("%I:%M %p"))
        response += appended
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description=response))
    
# Remove shows
@client.command()
async def removeshow(ctx, arg=None):
    if not (len(showlist) <= 0 or arg == None):
        try:
            if int(arg) <= len(showlist):
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="Removing **{}** at indice **{}**.".format(showlist[int(arg)].name, int(arg))))
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
            showlistf += "!klpi addshow \"{}\" \"{}\" {} {} {}\n".format(i.name, i.dj, i.day, datetime.strptime(i.starttime, "%H:%M").strftime("%H:%M"), datetime.strptime(i.endtime, "%H:%M").strftime("%H:%M"))
        file.write(showlistf)
    
    # send file to Discord in message
    with open("backup.txt", "rb") as file:
        await ctx.send("Here is the current showlist!", file=discord.File(file, "backup.txt"))

# Import backed up showlist
@client.command(name="import", pass_context=True)
async def importlist(ctx, array=None):
    if (array == None):
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="Command under construction..."))
        return
    '''else:
        local_list = []
        for i in array:
            # name, dj, day, starttime, endtime
            for h in range(0, 4):
                print(f"{i[h]}")
            newshow = Show(i[0], i[1], i[2], i[3], i[4])
            local_list.append(newshow)
        showlist = local_list
        '''
        

@client.command()
async def kill(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Executive Staff")
    if role in ctx.author.roles:
        print(f"Bot killed by {ctx.message.author}")
        await ctx.send(f'I have been slain by {ctx.message.author}...')
        exit()
    else:
        pass

client.run(api_token)
