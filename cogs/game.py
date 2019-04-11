"""Cog for games and fun."""
import discord
from discord.ext import commands
from utils.dbhandler import DBHandler


class GameCog:
    """Cog for games and fun."""

    def __init__(self, bot):
        """Initialize the cog."""
        print("Game cog Initialized")
        self.bot = bot
        self.dbhandler = DBHandler()

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coins(self, ctx, member: discord.Member = None):
        """Return a user's number of coins, or if no user, the authors."""
        if member is None:
            coins = self.dbhandler.getCoins(ctx.author.id)
            return await ctx.channel.send(f"`You have {coins} coins`")
        coins = self.dbhandler.getCoins(member.id)
        return await ctx.channel.send(f"`{member.name} has {coins} coins`")


def setup(bot):
    """Initialize and add to main script."""
    bot.add_cog(GameCog(bot))
