import discord
from discord.ext import commands
from discord_token import api_token

client = discord.Client()

class Show:
    def ___init__(self, name, dj, day, starttime):
        self.name = name
        self.dj = dj
        self.day = day
        self.starttime = starttime

shows = []

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!bot help'):
        if message.channel.name == 'exec-chat':
            await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description='Yo, whats up?'))
    if message.content.startswith('!bot addshow'):
        if message.channel.name == 'exec-chat' and message.author.role == :
            await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="What's the show name?"))
            show_name = await bot.wait.for('message', timeout=15)
            await message.channel.send(show_name)
    if message.content.startswith('!fobot addrole '):
        roleid = message.content.replace('!fobot addrole ', '').replace('-', '').replace(' ', '').replace('<', '').replace('>', '').replace(':', '').lower()
            if roleid in botroles:
                rolename = botroles[roleid]
                role = discord.utils.get(message.guild.roles, name=rolename)
                await message.channel.send(embed=discord.Embed(colour=discord.Colour(0x00ff00), description='**Success**: Role "' + role.name + '" added to "' + message.author.name + '"'))

client.run(api_token)
