import discord
from discord.ext import commands
from discord.ext.commands import guild_only, has_permissions
import time


class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot is Online')
        

    @commands.Cog.listener()
    async def on_member_join(self, ctx, member):
        await ctx.send(f'{member} has joined server')

    @commands.Cog.listener()
    async def on_member_remove(self, ctx, member):
        await ctx(f'{member} has left the server')

    @commands.command(name='help')
    async def help(self, ctx, cog=None):
        if cog is not None:
            for cog_class in self.client.cogs.values():
                if cog_class.qualified_name.lower() == cog.lower():
                    commands = cog_class.get_commands()
                    embed = discord.Embed(title=f"{cog_class.qualified_name} Commands", description="", color=discord.Color.blurple())
                    for command in commands:
                        if not command.hidden:
                            embed.add_field(name=f"**{command.name}**", value=command.help, inline=False)
                    await ctx.send(embed=embed)
                    return
            await ctx.send(f"I'm sorry, I couldn't find a cog named '{cog}'.")
        else:
            embed = discord.Embed(title="Help", description="List of available cogs:", color=discord.Color.blurple())
            for cog in self.bot.cogs.values():
                if cog.qualified_name.lower() != "help":
                    embed.add_field(name=cog.qualified_name, value=cog.description, inline=False)
            await ctx.send(embed=embed)

    @commands.command(name="ping",
                      description="Shows my ping.",
                      usage=""
                     )
    async def ping(self, ctx):
      channel = ctx.message.channel
      t1 = time.perf_counter()
      await channel.trigger_typing()
      t2 = time.perf_counter()
      ping = round((t2 - t1) * 1000)
      embed = discord.Embed(title=None,description=f'My ping is: {ping}ms',color=0x2874A6)
      await channel.send(embed=embed)

    @commands.command()
    async def rule(self, ctx):
        embed = discord.Embed(title="Server Rules", color=0x4378)
        embed.add_field(name="Rule 1", value="Be respectful: Treat all members with respect and refrain from using any derogatory language or making personal attacks.")
        embed.add_field(name="Rule 2", value="No spamming: Avoid flooding the chat with repeated messages or links. If you have something to share, do it once and wait for others to respond.")
        embed.add_field(name="Rule 3", value="No NSFW content: Do not share any explicit or offensive content that may be considered not safe for work. This includes links, images, or any other media.")
        embed.add_field(name="Rule 4", value="Follow Discord's ToS: Abide by the Discord's terms of service and community guidelines. Any violation of these rules can result in being kicked out of the server.")
        embed.add_field(name="Rule 5", value="Ask for help politely: If you need help, ask for it politely and wait for someone to respond. Do not demand or spam for assistance.")
        embed.add_field(name="Rule 6", value="Report any rule-breaking: If you see any member violating the rules, report it to the server admin or moderators immediately. Do not take matters into your own hands.")
        embed.set_footer(text="Breaking the rules may result in a warning or a ban. The owner and admins preserves the right to change the rules when deemed fit.")
        await ctx.send(embed=embed)

    # Commands for moderation
    @commands.command()
    async def clear(self, ctx, amount=5):
        await ctx.channel.purge(limit=amount + 1)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reasons=reason)
        ctx.send(f'{member} has been kicked from server')

    @commands.command(name="ban",
                      description="Bans member from server.",
                      usage="<user>")
    async def ban(self, ctx, member: discord.Member = None):
        author = ctx.message.author
        channel = ctx.message.channel
        user = member.name
        if author.guild_permissions.kick_members:
            await channel.send(f'{user} has been banned')
            await member.ban()
        else:
            await channel.send('You lack permission to perform this action')

    @commands.command(name="unban",
                      description="Unbans member from server.",
                      usage="<user>")
    @guild_only()
    async def unban(self, ctx, id: int):
        user = await self.client.fetch_user(id)
        await ctx.guild.unban(user)
        await ctx.send(
            f'{user.mention} welcome back! PLease make sure to read the #rules to avoid being banned.'
        )


async def setup(client):
    await client.add_cog(Moderation(client))
    print("Moderation Loaded")
