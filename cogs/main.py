"""Cog for main commands."""
import discord
from discord.ext import commands
from utils.consts import Consts
from utils.embedgenerator import Embed


class MainCog:
    """Main cog."""

    CONSTS = Consts()
    WAIT_BEFORE_DELETE = 3

    def __init__(self, bot):
        """Initialize the cog."""
        print("Main cog Initialized")
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def clear(self, ctx, number: int = 10):
        """Clear messages."""
        print("Clear called")
        if "administrator" in [y.name.lower() for y in ctx.author.roles]:
            if number > 0 and number < 75:
                deleted = await ctx.channel.purge(limit=number + 1)
                await ctx.channel.send(
                            f"Deleted {len(deleted) - 1} messages")
            return await ctx.channel.send(
                            "You can specify a number of messages (1 - 75)")
        return await ctx.channel.send(
                            "You don't have the `administrator` role!")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def whois(self, ctx, member: discord.Member = None):
        """Run when the whois command is called."""
        print("Whois called")
        embed = Embed([("Display Username", f":name_badge: {member.name}"),
                       ("Status", f":o:{str(member.status)}"),
                       ("Joined On", f":date: {member.joined_at.date()}"),
                       ("Role(s)", f":bow:" + ''.join(
                        [str(role.mention) for role in member.roles[1:]]))],
                            author=ctx.message.author,
                            thumbnail=member.avatar_url).generate_embed()
        await ctx.channel.send(embed=embed)


def setup(bot):
    """Initialize and add to main script."""
    bot.add_cog(MainCog(bot))
