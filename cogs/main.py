"""Cog for main commands."""
import datetime
import random
from dateutil.relativedelta import relativedelta
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
        if member is None:
            return await ctx.channel.send("Please do: ~whois @user")
        embed = Embed([("Display Username", f":name_badge: {member.name}"),
                       ("Status", f":o:{str(member.status)}"),
                       ("Joined On", f":date: {member.joined_at.date()}"),
                       ("Role(s)", f":bow:" + ''.join(
                        [str(role.mention) for role in member.roles[1:]]))])
        embed.author = ctx.message.author
        embed.thumbnail = member.avatar_url
        embed = embed.generate_embed()
        return await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def report(self, ctx, victim: discord.Member, reason: str):
        """Run when the report command is called."""
        if victim is None or reason is None:
            return await ctx.channel.send("Please do ~report <user> <reason>")
        for member in ctx.guild.members:
            for role in member.roles:
                print(f"{role.name} - {role.id}")
                # Administrator or owner
                if role.id in self.CONSTS.administrators:
                    try:
                        await member.send("{} reported {} for {}".format(
                                                ctx.author.name, victim, reason
                                                ))
                    # User has DMs from members disabled
                    except discord.errors.HTTPException:
                        pass
        return await ctx.channel.send(":white_check_mark: Thank you")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def echo(self, ctx, *args):
        """Run when the echo command is called."""
        if args is None:
            return await ctx.channel.send("Please do ~echo <message>")
        return await ctx.channel.send(f"`{' '.join([x for x in args])}`")

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def server(self, ctx):
        """Run when the server command is called - gives info about server."""
        guild = ctx.message.author.guild
        embed = Embed([("Server Name", f":name_badge: {guild.name}"),
                       ("Region", f":o:{guild.region}"),
                       ("Owner", f":person_with_blond_hair: {guild.owner}"),
                       ("Member Count", f":100: {guild.member_count}"),
                       ("Date Created", f":date: {guild.created_at}")])
        embed.thumbnail = guild.icon_url
        embed = embed.generate_embed()
        return await ctx.channel.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gcses(self, ctx):
        """Run when the gcse countdown command is called."""
        today = datetime.datetime.today()
        td = relativedelta(datetime.datetime(2019, 5, 13, 9, 0, 0), today)
        return await ctx.channel.send(
            "`{} months, {} weeks, {} days, {} hours {} minutes until GCSES!`"
            .format(
                td.months, td.weeks, td.days, td.hours, td.minutes
            ))

    @commands.command()
    @commands.cooldown(1, 1, commands.BucketType.user)
    async def roll(self, ctx):
        """Run when the roll command is called."""
        number = random.randint(1, 6)
        msg = await ctx.channel.send(f"`You rolled a {number}`")

        def check(self, user):
            """Check user integrity (check user != bot)."""
            return user.id != 563815182892138507
        await self.bot.wait_for('reaction_add', timeout=60.0,
                                check=check)
        return await msg.delete()


def setup(bot):
    """Initialize and add to main script."""
    bot.add_cog(MainCog(bot))
