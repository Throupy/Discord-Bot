"""Cog for main commands."""
import time
import discord
import threading
from discord.ext import commands


class MainCog:
    """Main cog."""

    WAIT_BEFORE_DELETE = 3

    def __init__(self, bot):
        """Initialize the cog."""
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def clear(self, ctx, number: int = 10):
        """Clear messages."""
        if "administrator" in [y.name.lower() for y in ctx.author.roles]:
            if number > 0 and number < 75:
                deleted = await ctx.channel.purge(limit=number + 1)
                return await ctx.channel.send(
                            f"Deleted {len(deleted) - 1} messages")
            return await ctx.channel.send(
                            "Please specify a number of messages (1 - 75)")
        return await ctx.channel.send(
                            "You don't have the `administrator` role!")


def setup(bot):
    """Initialize and add to main script."""
    bot.add_cog(MainCog(bot))
