import discord
from discord.ext import commands
from discord_token import api_token
import time

client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print(f'Success! {client.user} has awoken!')

@client.command()
async def ping(ctx):
    await ctx.send(f'<@&830141470345920544>')

@client.command()
async def test(ctx, arg):
    await ctx.send(arg)

@client.command()
async def kill(ctx):
    role = discord.utils.get(ctx.guild.roles, name="Executive Staff")
    if role in ctx.author.roles:
        await ctx.send(f'I have been slain...')
        exit()
    else:
        await ctx.send(f"Not exec staff!!")


client.run(api_token)
