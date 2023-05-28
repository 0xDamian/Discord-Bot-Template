import discord
from discord.ext import commands, tasks
import aiohttp
import os
from dotenv import load_dotenv

load_dotenv()
RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY')

class NewsCog(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel_id = 1095818905215316088 # Replace with the ID of the channel where you want to send the news
        self.news_task.start()

    def cog_unload(self):
        self.news_task.cancel()

    @tasks.loop(hours=1) # Set the time interval between news updates (in this case, 1 hour)
    async def news_task(self):
        channel = self.client.get_channel(self.channel_id)
        if channel:
            headers = {
                'x-rapidapi-host': "google-news-api1.p.rapidapi.com",
                'x-rapidapi-key': RAPIDAPI_KEY
            }
            async with aiohttp.ClientSession() as session:
                async with session.get("https://google-news-api1.p.rapidapi.com/search?language=EN&q=Cyber%20Security", headers=headers) as res:
                    json_dictionary = await res.json()
                    print(json_dictionary)
                    for item in json_dictionary['news']:
                        title = item['title']
                        url = item['link']
                        await channel.send(f"{title}\n{url}")

    @news_task.before_loop
    async def before_news_task(self):
        await self.client.wait_until_ready()

async def setup(client):
    await client.add_cog(NewsCog(client))
    print("News Loaded")
