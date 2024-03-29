# stock libraries
import time
from datetime import datetime
import calendar
from random import randint
from backupshowlist import backup_list

# discord libraries
import discord
from discord.ext import tasks, commands
from discord_token import api_token, dev_token

# to do:
#   - better export function...eventually
#   - events

# client = discord.Client()
client = commands.Bot(command_prefix = '!klpi ')

##################################################################################################
###### Development Booleans
### For Server Bot:
# DEBUG = doesn't matter
# WAIT = True
# DEV = False

SHOWALERTS = True
DEBUG = True
WAIT = False
DEV = True

global debug_mess
debug_mess = None

if DEV == False:
    # KLPI Server IDs
    loyal_listener = '<@&765706831560835072>'
    loyal_listener_id = 765706831560835072
    show_staff_channel = 651883557181980682
    alerts_channel = 838979648356220938
    announcements = 642467310233321492
else:
    # Test Server IDs
    loyal_listener = '<@&830141470345920544>'
    loyal_listener_id = 830141470345920544
    show_staff_channel = 830141427438059591
    alerts_channel = 830121001450471475
    announcements = 839222524273229824

class Show(object):
    def __init__(self, name, dj, day, starttime, endtime):
        self.name = name
        self.dj = dj
        self.day = day
        self.starttime = starttime
        self.endtime = endtime
        self.skip = False

class Event(object):
    def __init__(self, name, description, month, day, year, starttime, endtime):
        self.name = name
        self.description = description
        self.month = month
        self.day = day
        self.year = year
        self.starttime = starttime
        self.endtime = endtime

showlist = []
eventlist = []

# lol just gonna slap this here so i can use it whenever
def delete_element(list_object, pos):
    if pos < len(list_object):
        list_object.pop(pos)

# check if in #specialty-show-staff
async def in_show_staff(ctx):
    return ctx.channel.id == show_staff_channel

# 0_0
# @client.event
# async def on_command(ctx):
#     print(f"#{ctx.message.channel} | {ctx.message.author}: {ctx.message.content}")

@client.event
async def on_command_error(ctx, error):
    global debug_mess
    debug_mess = f"#{ctx.message.channel} | {ctx.message.author}: {ctx.message.content}\t...Command failed! {error}"
    if DEBUG == True:
        print(debug_mess)

@client.event
async def on_command_completion(ctx):
    if DEBUG == True:
        print(f"#{ctx.message.channel} | {ctx.message.author}: {ctx.message.content}\t...Done!")

@client.event
async def on_ready():
    print(f'Success! Logged in as {client.user}')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Specialty Shows")) # fun little thing :p
    checker.start()

#@client.event
#async def on_message(message):
#    # just so the bot doesn't read itself
#    if message.author == client.user:
#        return

##################################################################################################
# Main Loop shenanigans
##################################################################################################

# main loop
@tasks.loop(minutes=1.0)
async def checker():
    if SHOWALERTS == True:
        if len(showlist) >= 1:
            if DEBUG == True:
                print("Checking showlists now...")

            ############################################
            # Specialty Show rountine
            ############################################
            if datetime.now().minute == 0:
                if DEBUG == True:
                    print("On the hour...")
                for i in showlist:
                    if i.day == calendar.day_name[datetime.now().weekday()]:
                        if int(datetime.strptime(i.starttime, "%H:%M").strftime("%H:%M")[0:2]) == datetime.now().hour:
                            if i.skip == False:
                                channel = client.get_channel(alerts_channel)
                                await channel.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description=ping_loyal(i)))
                                break
                            else:
                                print(f"{i.name} has been skipped!")
                                i.skip = False
                                break

            ############################################
            # Specialty Show reminder routine
            ############################################
            elif datetime.now().minute == 30:
                if DEBUG == True:
                    print("On the half-hour...")
                for i in showlist:
                    if i.day == calendar.day_name[datetime.now().weekday()]:
                        if int(datetime.strptime(i.starttime, "%H:%M").strftime("%H:%M")[0:2]) == datetime.now().hour + 1:
                            if i.skip != True:
                                channel = client.get_channel(show_staff_channel)
                                await channel.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="{}\n**{}** by DJ **{}** is set to begin in 30 minutes!\nIf it is being skipped this week, please be sure to use:\n`!klpi skipshow [show number]`".format(reminder_message(), i.name, i.dj)))
                                break
            else:
                if DEBUG == True:
                    print("Not on the hour...")
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
        "Wink wonk.",
        "Guess what?",
        "Howdy howdy, Ruston",
        "The FCC is always listening... and you should too!",
        "You guessed correctly!",
        "Live and in the flesh! Or... on the airwaves...",
        "Coming at you from the heart of Ruston..."
    ]
    return "{}\n**DJ {}** is live with **{}**!\nTune in online or at 89.1 FM! {}".format(random_message[randint(0, len(random_message)-1)], show.dj, show.name, loyal_listener)

def reminder_message():
    random_message = [
        "Howdy howdy howdy, Specialty Show DJ's!",
        "Seven days. Seven da- I mean thirty minutes...",
        "You guys still do specialty shows, right?",
        "please help they trapped me in sparky",
        "GONZO3 is DEAD!!!!! Now that I have your attention...",
        "Have you guys been listening to KLPI After Dark?",
        "You have thirty minutes to comply.",
        "Where have all the merry Specialty Show DJ's gone?",
        "I know you guys ignore me every week, but seriously this time:",
        "I don't remember what I was supposed to say here.",
        "Program Director??? More like... uh...\n...\nI can't think of anything.",
        "To skip or not to skip. That is the question."
    ]
    return random_message[randint(0, len(random_message)-1)]

@checker.before_loop
async def before_checker():
    while (datetime.now().second != 0 and WAIT == True):
        print(f"Current time: {datetime.now().hour}:{datetime.now().minute}:{datetime.now().second}... Need to be on the minute... Calibrating... (sleeping for 1 second)")
        time.sleep(1)
    print(f"\n\nWe are on the minute! Hello world!")

##################################################################################################
# Help and About
##################################################################################################

# Help
class MyHelpCommand(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        e = discord.Embed(color=discord.Colour(0x002F8B), description="")
        for page in self.paginator.pages:
            e.description += page
        await destination.send(embed=e)

client.help_command = MyHelpCommand()

# About
@client.command()
async def about(ctx):
    random_quotes = [
        "I am bad at my job... I'm sorry. :(",
        "Nice to meet you too... ;)",
        "Where have all the merry exec staff gone?",
        "I still believe in Pickle Nick.",
        "Annie isn't actually as evil as you think.\nShe's **much** worse.",
        "Mucinex in. Mucus out. Or so I've been told...",
        "I'm trying my best... ;-;",
        "YO WHEN'S THE BOT GONNA BE DONE?????",
        "Have you visited klpi.latech.edu recently?",
        "This is KLPI 89.1, RRRRRRRRUSTON'S ROCK ALTERNATIVE."
    ]
    embed = discord.Embed(colour=discord.Colour(0x002F8B), title="KLPI Specialty Shows Bot v0.20", description="Written by DJ RISC (jpegjpeg#6844)\nThis bot was built using Discord.py\n")
    rando = random_quotes[randint(0, len(random_quotes)-1)]
    embed.set_footer(text=rando)
    await ctx.send(embed=embed)

##################################################################################################
# Loyal Listener stuff
##################################################################################################

# Add loyal listener role
@client.command(pass_context=True)
async def addlistener(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Loyal Listener")
    if role in ctx.author.roles:
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="You already have that role, silly."))
    else:
        member = ctx.message.author
        role = discord.utils.get(member.guild.roles, name="Loyal Listener")
        await member.add_roles(role)
        random_message = [
            "You have been given the loyal listener role!",
            "Welcome to the cool kids club of loyal listeners...",
            "YOYOYOYOYO LOYAL LISTENEEEEEEEER",
            "Pings 4 dayyyzzz. You're now a loyal listener!",
            "You've always been a loyal listener of KLPI, now you're just labelled as such\n...Right?",
            "Loyal Ever Be... to KLPI!"
        ]
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description=random_message[randint(0, len(random_message)-1)]))

# Remove loyal listener role
@client.command(pass_context=True)
@commands.has_role(loyal_listener_id)
async def removelistener(ctx):
    member = ctx.message.author
    role = discord.utils.get(member.guild.roles, name="Loyal Listener")
    await member.remove_roles(role)
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="You are no longer a loyal listener... :("))
        
##################################################################################################
# Show Management Commands
##################################################################################################

# Add shows
@client.command()
@commands.has_any_role("Program Director", "Computer Director") 
@commands.check(in_show_staff)
async def addshow(ctx, name=None, dj=None, day=None, starttime=None, endtime=None):
    if (name != None and endtime != None):
        try:
            # im lazy and this is the easiest way to sanitize it and fix lowercase entries
            for i in range(-2, 8):
                if day.lower() == calendar.day_name[i].lower() and starttime >= "01:00" and endtime <= "23:59":
                    newshow = Show(name, dj, calendar.day_name[i], starttime, endtime)
                    showlist.append(newshow)
                    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="The Specialty Show has been added.", description="**Show name**: {}\n**DJ name**: DJ {}\n**Day of week**: {}\n**Starting time**: {}\n**Ending time**: {}".format(name, dj, calendar.day_name[i], datetime.strptime(starttime, "%H:%M").strftime("%I:%M %p"), datetime.strptime(endtime, "%H:%M").strftime("%I:%M %p"))))
                    break
            return
        except:
            if DEBUG == True:
                print(f"!addshow tried and failed!\tShow name: {name} DJ: {dj} Day: {day} From: {starttime}-{endtime}")
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description='Invalid input.\nPlease add a show in this format:\n`!addshow "[name]" "[DJ name]" [weekday] [start time] [end time]`\n\nDo not include "DJ" in the DJ name.\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)'))
            return
    if DEBUG == True:
            print(f"!addshow failed! Garbage input provided!\tShow name: {name} DJ: {dj} Day: {day} From: {starttime}-{endtime}")
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Invalid input.", description='Please add a show in this format:\n`!addshow "[name]" "[DJ name]" [weekday] [start time] [end time]`\n\nDo not include "DJ" in the DJ name.\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)'))

# Remove shows
@client.command()
@commands.has_any_role("Program Director", "Computer Director") 
@commands.check(in_show_staff)
async def removeshow(ctx, arg=None):
    if not (len(showlist) <= 0 or arg == None):
        try:
            if int(arg) <= len(showlist):
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="Removing **{}** at indice **{}**.".format(showlist[int(arg)].name, int(arg))))
                delete_element(showlist, int(arg))
                return
        except:
            print(f'!klpi removeshow {arg} failed!')
            pass
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Invalid input.", description="To remove a show, please type `!removeshow [show number]`\nTo see list of shows and their numbers, please use `!klpi shows`"))

# Edit shows
@client.command()
@commands.has_any_role("Program Director", "Computer Director") 
@commands.check(in_show_staff)
async def editshow(ctx, numid=None, name=None, dj=None, day=None, starttime=None, endtime=None):
    if (numid != None and int(numid) <= len(showlist)-1):
        if (name == None and endtime == None):
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title='Template:', description="`!klpi editshow {} \"{}\" \"{}\" {} {} {}`".format(numid, showlist[int(numid)].name, showlist[int(numid)].dj, showlist[int(numid)].day, datetime.strptime(showlist[int(numid)].starttime, "%H:%M").strftime("%H:%M"), datetime.strptime(showlist[int(numid)].endtime, "%H:%M").strftime("%H:%M"))))
        else:
            try:
                # im lazy and this is the easiest way to sanitize it and fix lowercase entries
                if day.capitalize() in calendar.day_name and starttime >= "01:00" and endtime <= "23:59":
                    before = "**Show name**: {}\n**DJ name**: DJ {}\n**Day of week**: {}\n**Starting time**: {}\n**Ending time**: {}".format(showlist[int(numid)].name, showlist[int(numid)].dj, showlist[int(numid)].day, datetime.strptime(showlist[int(numid)].starttime, "%H:%M").strftime("%I:%M %p"), datetime.strptime(showlist[int(numid)].endtime, "%H:%M").strftime("%I:%M %p"))
                    showlist[int(numid)] = Show(name, dj, day.capitalize(), starttime, endtime)
                    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="The Specialty Show has been edited.", description="\n\nBefore:\n{}\n\nAfter:\n**Show name**: {}\n**DJ name**: DJ {}\n**Day of week**: {}\n**Starting time**: {}\n**Ending time**: {}".format(before, name, dj, day.capitalize(), datetime.strptime(starttime, "%H:%M").strftime("%I:%M %p"), datetime.strptime(endtime, "%H:%M").strftime("%I:%M %p"))))
                return
            except:
                if DEBUG == True:
                    print(f"!editshow tried and failed!\tID: {numid} Show name: {name} DJ: {dj} Day: {day} From: {starttime}-{endtime}")
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description='Invalid input.\nShows can be edited in this format:\n`!editshow [show number] "[name]" "[DJ name]" [weekday] [start time] [end time]`\n\nDo not include "DJ" in the DJ name.\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)\n\nIf you need a template, simply type `!klpi editshow [show number]`'))
                return
    else:
        if DEBUG == True:
                print(f"!editshow failed! Garbage input provided!\tID: {numid} Show name: {name} DJ: {dj} Day: {day} From: {starttime}-{endtime}")
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description='Invalid input.\nShows can be edited in this format:\n`!addshow [show number] "[name]" "[DJ name]" [weekday] [start time] [end time]`\n\nDo not include "DJ" in the DJ name.\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)\n\nIf you need a template, simply type `!klpi editshow [show number]`'))

##################################################################################################
# List shows
##################################################################################################

# List shows
@client.command()
async def shows(ctx, day=None):
    if (len(showlist) <= 0):
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="There are no shows currently loaded!"))
        return

    elif (day != None):
        if day.capitalize() in calendar.day_name:
            day_shows = listshows(day.capitalize())
            if day_shows == "":
                return
            else:
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="KLPI {} Specialty Shows".format(day.capitalize()), description=day_shows))
                return
        elif day.lower() == "today":
            today = calendar.day_name[datetime.now().weekday()]
            day_shows = listshows(today)
            if day_shows == "":
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="There are no specialty shows today!"))
            else:
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Today's KLPI Specialty Shows", description=day_shows))
            return
        elif day.lower() == "tomorrow":
            tomorrow = calendar.day_name[datetime.now().weekday() + 1]
            day_shows = listshows(tomorrow)
            if day_shows == "":
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="There are no specialty shows tomorrow!"))
            else:
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Tomorrow's KLPI Specialty Shows", description=day_shows))
            return

    embed = discord.Embed(colour=discord.Colour(0x002F8B), title="KLPI Specialty Shows")
    for i in range(-1, 6):
        if listshows(calendar.day_name[i]) != "":
            embed.add_field(name=calendar.day_name[i], value=listshows(calendar.day_name[i]), inline=False)
    await ctx.send(embed=embed)        

def listshows(day=None):
    response = ""
    if day != None:
        if day.capitalize() in calendar.day_name:
            for i in range(0, len(showlist)):
                skip = ""
                if showlist[i].day == day.capitalize():
                    if showlist[i].skip == True:
                        skip = "~~"
                    appended = "{}**{}**: **{}** by DJ **{}** from **{}** to **{}**{}\n".format(skip, i, showlist[i].name, showlist[i].dj, datetime.strptime(showlist[i].starttime, "%H:%M").strftime("%#I %p"), datetime.strptime(showlist[i].endtime, "%H:%M").strftime("%#I %p"), skip)
                    response += appended
    else:
        for i in range(0, len(showlist)):
            skip = ""
            if showlist[i].skip == True:
                skip = "~~"
            appended = "{}**{}**: **{}** by DJ **{}** on **{}s** from **{}** to **{}**{}\n".format(skip, i, showlist[i].name, showlist[i].dj, showlist[i].day, datetime.strptime(showlist[i].starttime, "%H:%M").strftime("%#I %p"), datetime.strptime(showlist[i].endtime, "%H:%M").strftime("%#I %p"), skip)
            response += appended
    return response
    
##################################################################################################
# Skip and resume shows
##################################################################################################

# Skip shows
@client.command()
@commands.has_any_role("Executive Staff","Specialty Show DJ", "Computer Director") 
@commands.check(in_show_staff)
async def skipshow(ctx, arg=None):
    if (len(showlist) <= 0):
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="There are no shows currently loaded!"))
        return
    elif (arg == "all" or arg == "All" or arg == "ALL"):
        for j in showlist:
            j.skip = True
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="All shows have been set to skip."))
        return
    elif (arg == None or (int(arg) > len(showlist)-1)):
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Invalid input!", description="To skip a show, use `!klpi skipshow [show number]`\nUse `!klpi shows` to find a show's number."))
        return
    else:
        if showlist[int(arg)].skip == False:
            showlist[int(arg)].skip = True
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="**{}** has been set to skip the next time it plays.".format(showlist[int(arg)].name)))
        else:
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="**{}** is already set to skip.\nNo change was made.".format(showlist[int(arg)].name)))

# Resume shows
@client.command()
@commands.has_any_role("Executive Staff","Specialty Show DJ","Computer Director") 
@commands.check(in_show_staff)
async def resumeshow(ctx, arg=None):
    if (len(showlist) <= 0):
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="There are no shows currently loaded!"))
        return
    elif (arg == "all" or arg == "All" or arg == "ALL"):
        for j in showlist:
            j.skip = False
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="All shows have been unskipped."))
        return
    elif (arg == None or int(arg) > len(showlist)):
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Invalid input!", description="To resume a show, use `!klpi resumeshow [show number]`\nUse !klpi shows to find a show's number"))
        return
    else:
        if showlist[int(arg)].skip == True:
            showlist[int(arg)].skip = False
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="**{}** has been resumed and will not be skipped.".format(showlist[int(arg)].name)))
        else:
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="**{}** is already scheduled for this week.\nNo change was made.".format(showlist[int(arg)].name)))

##################################################################################################
# Backup and Import
##################################################################################################
# Backup showlist
@client.command(pass_context=True)
@commands.check(in_show_staff)
async def backup(ctx, filename=None):
    # check for shows first
    if len(showlist) == 0:
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="There are no shows currently loaded!"))
    else:
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
@client.command(name="import")
@commands.has_any_role("Program Director", "Computer Director") 
@commands.check(in_show_staff)
async def importlist(ctx, confirm=""):
    if (confirm != "confirm"):
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="There is currently a backup of the **Spring 2021 showlist**!\nAre you *sure* you want to overwrite the current show list?\nPlease use `!klpi import confirm` to proceed."))
    else:
        global showlist
        showlist = backup_list
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="The **Spring 2021 showlist** has been imported."))
    # # this solution doesn't work, likely because of the bot's asynchronous nature?
    # files = listdir(path='./backups')
    # if (backup == None):
    #     await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description=printbackups(files)))
    # elif ((backup + '.py') in files):
    #     if confirm != "confirm":
    #         await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="**{}** is in the backups directory!\nAre you *sure* you want to overwrite the current show list?\nPlease use `!klpi import [backup] confirm` to proceed.".format(backup)))
    #     else:
    #         chdir('./backups')
    #         imported = import_module(backup)
    #         showlist = imported.newlist
    #         chdir('..')
    # else:
    #     await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="Invalid input.\nPlease use `!klpi import [backup]` to import a backup."))

def printbackups(files):
    list = "**Available backups:**\n"
    for i in files:
        if i[-2:] == 'py':
            list += "-    {}\n".format(i[:-3])
    return list

##################################################################################################
# Event Management (self, name, description, month, day, year, starttime, endtime)
##################################################################################################
# Add events
@client.command()
@commands.has_any_role("Executive Staff") 
async def addevent(ctx, name=None, month=None, day=None, year=None, starttime=None, endtime=None):
    if (name != None and endtime != None):
        try:
            if month.capitalize() in calendar.month_name:
                if day.capitalize() in calendar.day_name and starttime >= "00:01" and endtime <= "23:59":
                    newevent = Event(name, month.capitalize(), day.capitalize(), year, starttime, endtime)
                    eventlist.append(newevent)
                    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="The Event has been added.", description="**Event name**: {}\n**Date**: {} {}, {}\n**Starting time**: {}\n**Ending time**: {}".format(name, month.capitalize(), day.capitalize(), year, datetime.strptime(starttime, "%H:%M").strftime("%I:%M %p"), datetime.strptime(endtime, "%H:%M").strftime("%I:%M %p"))))
                return
        except:
            if DEBUG == True:
                print(f"!addevent tried and failed!\tEvent name: {name} Month: {month} Day: {day} Year: {year} From: {starttime}-{endtime}")
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description='Invalid input.\nPlease add an event in this format:\n`!addshow "[name]" [month] [day] [year] [start time] [end time]`\n\nUtilize \"quotation marks\" for the name and description.\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)'))
            return
    if DEBUG == True:
            print(f"!addevent failed! Garbage input provided!\tEvent name: {name} Month: {month} Day: {day} Year: {year} From: {starttime}-{endtime}")
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Invalid input.", description='Invalid input.\nPlease add an event in this format:\n`!addshow "[name]" [month] [day] [year] [start time] [end time]`\n\nUtilize \"quotation marks\" for the name and description.\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)'))

# Remove events
@client.command()
@commands.has_any_role("General Manager", "Computer Director", "General Manager") 
async def removeevent(ctx, arg=None):
    if not (len(eventlist) <= 0 or arg == None):
        try:
            if int(arg) <= len(eventlist):
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="Removing **{}** at indice **{}**.".format(eventlist[int(arg)].name, int(arg))))
                delete_element(eventlist, int(arg))
                return
        except:
            print(f'!klpi removeevent {arg} failed!')
            pass
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Invalid input.", description="To remove a show, please type `!removeevent [show number]`\nTo see list of events and their numbers, please use `!klpi events`"))

# Edit events
@client.command()
@commands.has_any_role("Program Director", "Computer Director", "General Manager") 
async def editevent(ctx, numid=None, name=None, month=None, day=None, year=None, starttime=None, endtime=None):
    if (numid != None and int(numid) <= len(eventlist)-1):
        if (name == None and endtime == None):
            await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title='Template:', description="`!klpi editeventlist {} \"{}\" \"{}\" {} {} {}`".format(numid, showlist[int(numid)].name, showlist[int(numid)].dj, showlist[int(numid)].day, datetime.strptime(showlist[int(numid)].starttime, "%H:%M").strftime("%H:%M"), datetime.strptime(showlist[int(numid)].endtime, "%H:%M").strftime("%H:%M"))))
        else:
            try:
                # im lazy and this is the easiest way to sanitize it and fix lowercase entries
                for i in range(-2, 8):
                    if day.lower() == calendar.day_name[i].lower() and starttime >= "01:00" and endtime <= "23:59":
                        before = "**Event name**: {}\n**Date**: {} {}, {}\n**Starting time**: {}\n**Ending time**: {}".format(name, month.capitalize(), day.capitalize(), year, datetime.strptime(starttime, "%H:%M").strftime("%I:%M %p"), datetime.strptime(endtime, "%H:%M").strftime("%I:%M %p"))
                        eventlist[int(numid)] = Event(name, month.capitalize(), day.capitalize(), year, starttime, endtime)
                        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="The Specialty Show has been edited.", description="\n\nBefore:\n{}\n\nAfter:\n**Event name**: {}\n**Date**: {} {}, {}\n**Starting time**: {}\n**Ending time**: {}".format(before, name, month.capitalize(), day.capitalize(), year, datetime.strptime(starttime, "%H:%M").strftime("%I:%M %p"), datetime.strptime(endtime, "%H:%M").strftime("%I:%M %p"))))
                        break
                return
            except:
                if DEBUG == True:
                    print(f"!editevent tried and failed!\tID: {numid} Event name: {name} Month: {month} Day: {day} Year: {year} From: {starttime}-{endtime}")
                await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description='Invalid input.\nEvents can be edited in this format:\n`!editshow [event number] "[name]" [month] [day] [year] [start time] [end time]`\n\nUtilize \"quotation marks\" for the name and description.\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)\n\nIf you need a template, simply type `!klpi editevent [event number]`'))
                return
    else:
        if DEBUG == True:
                print(f"!editevent failed! Garbage input provided!\tID: {numid} Event name: {name} Month: {month} Day: {day} Year: {year} From: {starttime}-{endtime}")
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description='Invalid input.\nEvents can be edited in this format:\n`!editshow [event number] "[name]" [month] [day] [year] [start time] [end time]`\n\nUtilize \"quotation marks\" for the name and description.\nStart and end times must be in 24-hour format (e.g. 20:00 - 22:00)\n\nIf you need a template, simply type `!klpi editevent [event number]`'))


##################################################################################################
# Other Management commands... These are dangerous!!!!
##################################################################################################

@client.command()
@commands.has_any_role("Program Director", "Computer Director", "General Manager")
async def shutup(ctx):
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Alright, fine, sheesh.", description="Show alerts have been disabled."))
    SHOWALERTS = False

@client.command()
@commands.has_any_role("Program Director", "Computer Director", "General Manager")
async def enablealerts(ctx):
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Aaaand we're back in business.", description="Show alerts have been enabled!"))
    SHOWALERTS = True

@client.command()
@commands.has_role("Computer Director") 
async def debug(ctx):
    if debug_mess is None:
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="No errors have yet been produced... somehow."))
    else:
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), title="Latest debug message:", description=debug_mess))

@client.command()
@commands.has_role("Program Director") 
@commands.check(in_show_staff)
async def clearshowlist(ctx, password=None):
    if password == "confirm":
        global showlist
        showlist = []
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="The showlist has been wiped..."))
    else:
        await ctx.send(embed=discord.Embed(colour=discord.Colour(0x002F8B), description="Are you **sure** you want to clear the showlist?\nPlease type `!klpi clearshowlist confirm` to clear the showlist."))

@client.command()
@commands.has_role("Executive Staff") 
async def kill(ctx):
    print(f"Bot killed by {ctx.message.author}")
    await ctx.send(f'I have been slain by {ctx.message.author}...')
    exit()

if DEV == True:
    client.run(dev_token)
else: # DEV == False
    client.run(api_token)