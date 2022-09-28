import discord
from discord.ext import commands

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client
        async def cog_load(self):


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

            # Commands for moderation
            @commands.command()
            async def clear(self, ctx, amount=5):
                await ctx.channel.purge(limit=amount + 1)
                await ctx.send(f'{amount} messages were deleted')

            @commands.command()
            async def kick(self, ctx, member: discord.Member, *, reason=None):
                await member.kick(reasons=reason)
                ctx.send(f'{member} has been kicked from server')

            @commands.command()
            async def ban(self, ctx, member: discord.Member, *, reason=None):
                await member.ban(reason=reason)
                await ctx.send(f'{member.mention} has been banned from server')

            @commands.command()
            async def unban(self, ctx, *, member):
                banned_users = await ctx.guild.bans()
                member_name, member_discriminator = member.split('#')
                for ban_entry in banned_users:
                    user = ban_entry.user

                    if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
                        await ctx.guild.unban(user)
                        await ctx.send(f'Unbanned {user.mention}')
                        return


def setup(client):
    await client.add_cog(Moderation(client))
      