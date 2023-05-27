import discord
from discord.ext import commands, tasks
import requests
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.environ['GOOGLE_NEWS_API_KEY']

class News(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.channel_id = 1095818905215316088
        self.url = f'https://newsapi.org/v2/top-headlines?q=cybersecurity&sources=google-news&apiKey={api_key}' # Create environment variable
        self.post_news.start()

    def cog_unload(self):
        self.post_news.cancel()

    @tasks.loop(hours=1) # Set the interval for how often you want to check for new news
    async def post_news(self):
        channel = self.client.get_channel(self.channel_id)
        response = requests.get(self.url)
        data = response.json()
        for article in data['articles']:
            embed = discord.Embed(title=article['title'], url=article['url'], description=article['description'])
            await channel.send(embed=embed)

    @post_news.before_loop
    async def before_post_news(self):
        await self.client.wait_until_ready()

async def setup(client):
    await client.add_cog(News(client))
    print("News Loaded")