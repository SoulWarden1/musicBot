import discord
from discord.ext import commands
from discord.utils import get
from random import randint
from datetime import datetime
import asyncio
import functools
import itertools
import math
import random

import discord
import youtube_dl
from async_timeout import timeout

class musicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=["Join"])
    async def join(self, ctx, *, channel: discord.VoiceChannel = None):
        try: # Attempts to find the authors vc or an inputted vc
            destination = channel or ctx.author.voice.channel 
        except: # If not vc is specified or the author is not in a vc, returns a message
            await ctx.reply("Please join a vc or specify a channel")
        else: # If successful
            # Trys to get the voice client obj for the current server
            voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
            if voice_client is not None: # If there is a voice client obj, move the bot
                await ctx.guild.voice_client.move_to(destination)
                await ctx.reply("Bot moved")
            else: # If the isn't a voice client obj, connect the bot
                await destination.connect()
                await ctx.reply("Bot connected")
            
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=["Disconnect","dc"])
    async def disconnect(self, ctx):
        if ctx.voice_client: # If the bot is in a voice channel 
            await ctx.guild.voice_client.disconnect() # Leave the channel
            await ctx.reply('Bot disconnected')
        else: # If the bot is not in a vc
            await ctx.reply("I'm not currently in a vc")
         
    # Volume
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='volume')
    async def _volume(self, ctx, volume: int):
        if not ctx.voice_state.is_playing:
            return await ctx.reply('Nothing is being played')

        if 0 > volume > 100:
            return await ctx.reply('Volume must be between 0 and 100')

        ctx.voice_state.volume = volume / 100
        await ctx.send(f'Volume of the player set to {volume}%')

def setup(bot):
    bot.add_cog(musicCog(bot))
