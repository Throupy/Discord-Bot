"""Embed generator to make for easier embed generation."""
import discord


class Embed:
    """Embed generator class."""

    def __init__(self, fields: list, colour=0xff0000,
                 author=None, thumbnail=None):
        """Initialize."""
        self.fields = fields
        self.thumbnail = thumbnail
        self.author = author
        self.colour = colour

    def generate_embed(self):
        """Generate the embed and return it."""
        embed = discord.Embed(color=self.colour)
        for i in range(0, len(self.fields)):
            embed.add_field(name=f"{self.fields[i][0]}",
                            value=f"{self.fields[i][1]}", inline=False)
        if self.author is not None:
            embed.set_footer(text=f"Called By {self.author}")
        if self.thumbnail is not None:
            embed.set_thumbnail(url=self.thumbnail)
        return embed
