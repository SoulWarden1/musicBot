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

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.2):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename
    
class musicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(aliases=["Join","connect","Connect"])
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
            await ctx.reply("The bot is not currently in a vc")
         
    # Volume
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='volume')
    async def volume(self, ctx, volume: int):
        voice_client = ctx.message.guild.voice_client
        if not voice_client.is_playing:
            return await ctx.reply('Nothing is being played')

        if 0 > volume > 100:
            return await ctx.reply('Volume must be between 0 and 100')

        voice_client.volume = volume / 100
        await ctx.reply(f'Volume of the player set to {volume}%')
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only() 
    @commands.command(name = "play")
    async def play(self,ctx,url):
        try :
            server = ctx.message.guild
            voice_channel = server.voice_client

            async with ctx.typing():
                filename = await YTDLSource.from_url(url, loop=self.bot.loop)
                voice_channel.play(discord.FFmpegPCMAudio(executable="ffmpeg.exe", source=filename))
            await ctx.reply('**Now playing:** {}'.format(filename))
        except:
            await ctx.reply("An error has occurred")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self,ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.pause()
            await ctx.reply("Paused")
        else:
            await ctx.reply("The bot is not playing anything at the moment")
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()   
    @commands.command(name='resume', help='Resumes the song')
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_paused():
            await voice_client.resume()
            await ctx.reply("Playing")
        else:
            await ctx.reply("The bot was not playing anything before this. Use play_song command")

    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.guild_only()
    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            await voice_client.stop()
            await ctx.reply("Stopping")
        else:
            await ctx.reply("The bot is not playing anything at the moment")

def setup(bot):
    bot.add_cog(musicCog(bot))
