import discord
from discord.ext import commands


class ErrorCog(commands.Cog, name='Error'):

    def __init__(self, client):

        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if hasattr(ctx.command, 'on_error'):
                return
            else:
                embed = discord.Embed(
                    title=f'Error in {ctx.command}:',
                    description=
                    f'```{ctx.command.qualified_name} {ctx.command.signature} \n{error}```',
                    colour=0x4378)
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title=f'Error in {ctx.command}:',
                                  description=f'```{error}```',
                                  colour=0x4378)
            await ctx.send(embed=embed)


async def setup(client, ctx):
    await client.add_cog(ErrorCog(client))
    await ctx.send("Error Loaded")
    print("Error Loaded")
