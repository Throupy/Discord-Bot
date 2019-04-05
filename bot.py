"""The script runs the bot."""
import os
import asyncio
from discord.ext import commands
from discord.utils import get
import discord
from utils.consts import Consts

consts = Consts()
bot = commands.Bot(command_prefix="~",
                   status=discord.Status.online,
                   activity=discord.Game(name="Fucking bitches"))

@bot.event
async def on_ready():
    """Run when the bot is ready."""
    print("Ready to go!")
    print(f"Serving: {len(bot.guilds)} servers!")
    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Game(name="Fucking bitches"))


@bot.event
async def on_member_join(ctx):
    """Run when a new member joins."""
    channel = get(bot.get_all_channels(),
                  guild__name='Lube Lads',
                  name='welcome')
    await ctx.send(consts.welcomeDMMessage.format(ctx.name))
    msg = await channel.send(
        f"Welcome, {ctx.mention} If you agree with the rules please react to the message"
    )
    reaction, user = await bot.wait_for('reaction_add')
    role = get(ctx.guild.roles, name='Member')
    await ctx.add_roles(role)


@bot.event
async def on_member_ban(ctx, member):
    """Run when a member gets banned (probably kacper)."""
    channel = get(bot.get_all_channels(),
                  guild__name="Lube Lads",
                  name="announcements")
    await channel.send(f"{member.name} Just got banned from the server")

@bot.event
async def on_message(message):
    channel = get(bot.get_all_channels(),
                  guild__name="Lube Lads",
                  name="announcements")
    if message.channel.id == channel.id:
        # If the message was NOT send by the bot
        if message.author != bot:
            await message.pin()
            # Remove the crappy pin message
            await message.channel.purge(limit=1)

bot.load_extension("cogs.error_handler")
bot.load_extension("cogs.main")
token = os.environ.get("DISCORD_BOT_TOKEN")
bot.run(token)
