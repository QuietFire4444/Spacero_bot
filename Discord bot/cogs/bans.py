import discord
from discord.ext import commands
from main import SUPER_PROTECTED_ROLE_NAME, PROTECTED_ROLE_NAME, previous_roles, log_action, can_ban

class BanCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @can_ban()
    async def ban(self, ctx, member: discord.Member):
        await ctx.message.delete()
        banned_role_name = "Banned"
        banned_role = discord.utils.get(ctx.guild.roles, name=banned_role_name)

        if not banned_role:
            banned_role = await ctx.guild.create_role(name=banned_role_name)
            await ctx.send(f"Created role '{banned_role_name}'")

        if discord.utils.get(member.roles, name=SUPER_PROTECTED_ROLE_NAME):
            await ctx.send(f"? You cannot ban a member with the '{SUPER_PROTECTED_ROLE_NAME}' role.")
            return

        if discord.utils.get(member.roles, name=PROTECTED_ROLE_NAME) and not ctx.author.guild_permissions.administrator:
            await ctx.send(f"? You cannot ban a member with the '{PROTECTED_ROLE_NAME}' role.")
            return

        try:
            previous_roles[member.id] = [role for role in member.roles if role != ctx.guild.default_role]
            await member.edit(roles=[])
            await member.add_roles(banned_role)
            await log_action(ctx, "Ban", member)

            embed = discord.Embed(
                title="User Banned",
                description=f"{member.mention} has been banned.",
                color=discord.Color.red()
            )
            embed.set_footer(text=f"Command issued by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await ctx.send(f"{ctx.author.mention}", embed=embed)

        except discord.Forbidden:
            await ctx.send("? I do not have permission to manage roles for that user.")
        except discord.HTTPException as e:
            await ctx.send(f"? An error occurred: {e}")

    @commands.command(name="unban")
    @can_ban()
    async def unban(self, ctx, member: discord.Member):
        await ctx.message.delete()
        banned_role_name = "Banned"
        banned_role = discord.utils.get(ctx.guild.roles, name=banned_role_name)

        if member.id not in previous_roles:
            await ctx.send(f"? No record of previous roles for {member.mention}.")
            return

        try:
            if banned_role in member.roles:
                await member.remove_roles(banned_role)

            roles_to_restore = [role for role in previous_roles[member.id] if role in ctx.guild.roles]
            await member.add_roles(*roles_to_restore)
            await log_action(ctx, "Unban", member)

            embed = discord.Embed(
                title="User Unbanned",
                description=f"{member.mention} has been unbanned.",
                color=discord.Color.green()
            )
            embed.set_footer(text=f"Command issued by {ctx.author}", icon_url=ctx.author.display_avatar.url)
            await ctx.send(f"{ctx.author.mention}", embed=embed)

            del previous_roles[member.id]

        except discord.Forbidden:
            await ctx.send("? I do not have permission to manage roles for that user.")
        except discord.HTTPException as e:
            await ctx.send(f"? An error occurred: {e}")


# THIS IS THE ONLY THING THAT SHOULD BE CALLED OUTSIDE A CLASS IN THIS FILE
def setup(bot):
    bot.add_cog(BanCommands(bot))