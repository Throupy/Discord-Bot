"""Cogs for audio."""
import random
import os
import discord
from discord.ext import commands


class AudioCog:
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


def setup(bot):
    """Initialize and add to main script."""
    bot.add_cog(AudioCog(bot))
