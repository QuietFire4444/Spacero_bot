# cogs/config_commands.py

from discord.ext import commands
from config_manager import config

class ConfigCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def has_permission(self, ctx):
        user_id = ctx.author.id
        user_roles = [r.name.lower() for r in ctx.author.roles]
        admin_roles = [r.lower() for r in config.get("permissions.admin_roles", [])]
        allowed_users = config.get("permissions.allowed_users", [])

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
