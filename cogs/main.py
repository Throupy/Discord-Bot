"""Cog for main commands."""


class MainCog:
    """Main cog."""

    def __init__(self, bot):
        """Initialize the cog."""
        self.bot = bot


def setup(bot):
    """Initialize and add to main script."""
    bot.add_cog(MainCog(bot))
