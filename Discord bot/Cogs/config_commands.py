# cogs/config_commands.py

from discord.ext import commands
from config_manager import config

class ConfigCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_permission(self, ctx):
        roles = [r.name for r in ctx.author.roles]
        return (
            any(role in config.get("permissions.admin_roles", []) for role in roles) or
            ctx.author.id in config.get("permissions.allowed_users", [])
        )

    @commands.command()
    async def toggle_feature(self, ctx, feature: str):
        features = config.get("features", {})
        if not self.has_permission(ctx):
            await ctx.send("❌ You do not have permission to modify settings.")
            return

        if feature not in features:
            await ctx.send(f"❓ Feature `{feature}` not found.")
            return

        new_val = config.toggle(f"features.{feature}")
        await ctx.send(f"🔄 Feature `{feature}` toggled to `{new_val}`")

async def setup(bot):
    await bot.add_cog(ConfigCommands(bot))
