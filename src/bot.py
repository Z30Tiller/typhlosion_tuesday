import os
import discord

from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = init(os.getenv('CHANNEL_ID'))

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# List of Tuesday GIF URLs
tuesdayGifs = [
    'https://tenor.com/en-GB/view/typhlosion-tuesday-meme-gif-5109207821042719955',
    'https://tenor.com/en-GB/view/typhlosion-tuesday-meme-tuesday-poke-meme-gif-26753999',
    'https://tenor.com/en-GB/view/happy-typhlosion-tuesday-meme-gif-4051929047719001080'
]

# List of Wednesday GIF URLs
wednesdayGifs = [
    'https://tenor.com/en-GB/view/pokemon-typhlosion-tuesday-gif-12713113255833901878'
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

    # Schedule the job to run every Tuesday at 12:00 PM
    scheduler = AsyncIOScheduler()
    scheduler.add_job(post_tue_gifs, 'cron', day_of_week='tue', hour=8, minute=0)
    scheduler.add_job(post_wed_gifs, 'cron', day_of_week='wed', hour=8, minute=0)
    scheduler.start()

async def post_tue_gifs():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        for gif in tuesdayGifs:
            await channel.send(gif)

async def post_wed_gifs():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        for gif in wednesdayGifs:
            await channel.send(gif)

bot.run(TOKEN)