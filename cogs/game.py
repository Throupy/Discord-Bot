"""Cog for games and fun."""
import random
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

    @commands.command(aliases=['bal', 'balance'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def coins(self, ctx, member: discord.Member = None):
        """Return a user's number of coins, or if no user, the authors."""
        if member is None:
            coins = self.dbhandler.getCoins(ctx.author.id)
            return await ctx.channel.send(f"`You have {coins} coins`")
        coins = self.dbhandler.getCoins(member.id)
        return await ctx.channel.send(f"`{member.name} has {coins} coins`")

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def work(self, ctx):
        """Work and get money."""
        salary = random.randint(10, 100)
        self.dbhandler.addCoins(ctx.author.id, salary)
        return await ctx.channel.send(f"`You worked and got {salary} coins`")

    @commands.command()
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def crime(self, ctx):
        """Commit a crime and get money."""
        if random.randint(1, 2) == 1:
            gained = random.randint(100, 500)
            self.dbhandler.addCoins(ctx.author.id, gained)
            await ctx.channel.send(
                            f"`You committed a crime and got {gained}`")
        else:
            toSubtract = round(self.dbhandler.getCoins(ctx.author.id) * 0.03)
            self.dbhandler.subtractCoins(ctx.author.id, toSubtract)
            await ctx.channel.send(
                                f"`You were caught and lost 3% of your coins`")
        newAmt = self.dbhandler.getCoins(ctx.author.id)
        return await ctx.channel.send(
                                f"`Your new balance is {newAmt}`")



def setup(bot):
    """Initialize and add to main script."""
    bot.add_cog(GameCog(bot))
