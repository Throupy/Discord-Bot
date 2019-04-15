"""Cogs for audio."""
import urllib
import re
import random
import os
import asyncio
import youtube_dl
import discord
from discord.ext import commands
from utils.consts import Consts

CONSTS = Consts()
ytdl = youtube_dl.YoutubeDL(CONSTS.ytdl_format_options)


# https://github.com/Rapptz/discord.py/blob/rewrite/examples/basic_voice.py
# This class is taken from here and I have made a few adjustments
class YTDLSource(discord.PCMVolumeTransformer):
    """Get source (youtube DL)."""

    def __init__(self, source, *, data, volume=0.5):
        """Initialize."""
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, strm=False):
        """Get video from URL."""
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None,
                                          lambda:
                                          ytdl.extract_info(url,
                                                            download=not strm))

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if strm else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename,
                                          **CONSTS.ffmpeg_options), data=data)


class AudioCog(commands.Cog):
    """Cog for audio."""

    def __init__(self, bot):
        """Initialize the bot."""
        self.bot = bot

    @commands.command(aliases=['nanny', 'randomburfz'])
    async def burfz(self, ctx):
        """Run when the burfz command is called."""
        try:
            if ctx.author.voice is not None:
                if ctx.voice_client is not None:
                    await ctx.voice_client.move_to(ctx.author.voice.channel)
                else:
                    await ctx.author.voice.channel.connect()
            else:
                return await ctx.channel.send(":x: Not in voice channel")
            burfVid = 'burfz/' + random.choice(os.listdir('burfz/'))
            source = discord.PCMVolumeTransformer(
                                            discord.FFmpegPCMAudio(burfVid))
            return await ctx.voice_client.play(source)
        except discord.errors.ClientException:
            await ctx.channel.send(":x: Already playing audio")
        except TypeError:
            pass

    @commands.command(aliases=['p'])
    async def play(self, ctx, *, search=None):
        """Run when the play commands is called."""
        if search is None:
            return await ctx.channel.send("Please do +play <search/URL>")
        if search[0:4] == 'http':
            url = search
        else:
            query_string = urllib.parse.urlencode({
                'search_query': search
            })
            htm_content = urllib.request.urlopen(
                'https://youtube.com/results?' + query_string
            )
            searchResults = re.findall('href=\"\\/watch\\?v=(.{11})',
                                       htm_content.read().decode())
            url = 'http://youtube.com/watch?v=' + searchResults[0]
        if ctx.author.voice is not None:
            if ctx.voice_client is not None:
                await ctx.voice_client.move_to(ctx.author.voice.channel)
            else:
                await ctx.author.voice.channel.connect()
        else:
            return await ctx.channel.send(":x: Not in voice channel")
        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop,
                                               strm=True)
            ctx.voice_client.play(player,
                                  after=lambda e:
                                  print('Player error: %s' % e) if e else None)
        await ctx.send('Now playing: {}'.format(player.title))

    @commands.command()
    async def stop(self, ctx):
        """Stop the playing video, if any."""
        return ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        """Pause the currently playing video."""
        if ctx.voice_client.is_playing():
            return ctx.voice_client.pause()
        return await ctx.channel.send("`Nothing is playing`")

    @commands.command(aliases=['resume'])
    async def unpause(self, ctx):
        """Unpause the video."""
        if ctx.voice_client.is_paused():
            return ctx.voice_client.resume()
        return await ctx.channel.send("`Nothing is paused`")

    @commands.command(aliases=['dc', 'leave'])
    async def disconnect(self, ctx):
        """Disconnect the bot."""
        return await ctx.voice_client.disconnect()


def setup(bot):
    """Initialize and add to main script."""
    bot.add_cog(AudioCog(bot))
