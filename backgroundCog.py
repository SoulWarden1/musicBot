from datetime import datetime
import discord
from discord.ext import commands
from discord.ext import tasks
from random import randint, choice
import asyncio

class backgroundCog(commands.Cog):
    def __init__(self, bot):
        # Initialises cog
        self.bot = bot

    # Rotates the status
    @tasks.loop(seconds=30.0)
    async def statusRotation(self):
        # List of possible statuses
        statuses = ["+help","music","BASS"]
        # Changes bot status
        await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{choice(statuses)}"))

    @commands.Cog.listener()
    async def on_ready(self):
        # Creates background loops
        self.statusRotation.start()
        # Prints the successful start of the background task
        print("Background tasks started")
        
# Starts the cog
def setup(bot):
    bot.add_cog(backgroundCog(bot))
