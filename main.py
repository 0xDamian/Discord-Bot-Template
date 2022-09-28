
import discord
import asyncio
import os
from discord.ext import commands

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix='!', help_command=None)

# loads the extenstions
@client.command()
async def load(ctx, extension):
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            
# E no really concern me sha, 
# but if you want the cogs to load without having to type in a command, meaning loading the cogs as the bot starts up
# you can delete or comment out unload() & reload() at this point

"""
async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
         
async def main():
  await load()
  await client.start('abcd.1234.ABCD')
  
asyncio.run(main())
"""

@client.command()
async def unload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')


@client.command()
async def reload(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')
    await client.load_extension(f'cogs.{extension}')

# You can also just put the token here. Again, e no actually concern me
# I'm just doing the most
"""
client.run('abcd.1234.ABCD')
"""
client.run(os.getenv('TOKEN'))

