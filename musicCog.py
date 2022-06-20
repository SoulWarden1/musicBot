import discord
from discord.ext import commands
from discord.utils import get
from random import randint
from datetime import datetime
import asyncio

class musicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

def setup(bot):
    bot.add_cog(musicCog(bot))
