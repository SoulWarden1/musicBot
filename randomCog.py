import discord
from discord.ext import commands
from discord.utils import get
from random import randint
from datetime import datetime
import asyncio
import time

class randomCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    #Ping command
    @commands.cooldown(1, 2, commands.BucketType.user)
    @commands.command(aliases=["pong", "Ping", "Pong"])
    async def ping(self,ctx):
        if ctx.invoked_with == "ping" or ctx.invoked_with == "Ping": txt = "Pong"
        else: txt = "Ping"
        start_time = time.time()
        message = await ctx.send("Testing Ping...")
        end_time = time.time()

        await message.edit(content=f"{txt}!\nResponse Time: {round(self.bot.latency * 1000)}ms\nAPI Latency: {round(((end_time - start_time)-self.bot.latency) * 1000)}ms\nTotal Latency: {round((end_time - start_time) * 1000)}ms")

def setup(bot):
    bot.add_cog(randomCog(bot))
