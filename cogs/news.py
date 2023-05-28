import discord
from discord.ext import commands, tasks
import requests
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
            # Connect to the Google News API
            url = "https://google-news-api1.p.rapidapi.com/search"
            querystring = {"language": "EN", "q": "Cyber Security"}
            headers = {
                "X-RapidAPI-Key": RAPIDAPI_KEY,
                "X-RapidAPI-Host": "google-news-api1.p.rapidapi.com"
            }
            response = requests.get(url, headers=headers, params=querystring)
            json_dictionary = response.json()
            # Loop through dictionary keys to access each article
            for item in json_dictionary['articles']:
                # Pull the title and url for this article into variables.
                title = item['title']
                url = item['link']
                # Send the title and url to the specified channel
                await channel.send(f"{title}\n{url}")

    @news_task.before_loop
    async def before_news_task(self):
        await self.client.wait_until_ready()

async def setup(client):
    await client.add_cog(NewsCog(client))
    print("News Loaded")