from datetime import date, datetime

import discord
from discord.ext import commands, tasks
from discord_token import api_token

client = commands.Bot(command_prefix = '!')

class myCog(commands.Cog):
    def __init__(self):
        self.index = 0
        self.printer.start()

    def cog_unload(self):
        self.printer.cancel()

    @tasks.loop(seconds=5.0)
    async def printer(self):
        print(self.index)
        self.index += 1
"""
@tasks.loop(hours=1)
async def set_schedules(ctx):
    await ctx.send(embed=discord.Embed(colour=discord.Colour(0x00ffff), description="Top of the day!"))

@set_schedules.before_loop
async def before(ctx):
    print("Entering loop...")
    await set_schedules(ctx)
    print("Finished waiting")
"""
client.run(api_token)