import os
import discord

from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

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
    scheduler.add_job(post_tue_gifs, 'cron', day_of_week='tue', hour=10, minute=0)
    scheduler.add_job(post_wed_gifs, 'cron', day_of_week='wed', hour=10, minute=0)
    scheduler.start()

@bot.event
async def on_guild_join(guild):
    # This event is triggered when the bot joins a new server
    print(f"Bot added to server: {guild.name} (ID: {guild.id})")

    # You can choose a default channel to send a message to or configure further
    # Generally, try to find the 'general' text channel or the first channel
    for channel in guild.text.channels:
        if "general" in channel.name:
            await channel.send("Hello! Thanks for adding me to your server!")
            break
        else:
            # Fallback to the first available text channel
            first_channel = guild.text_channels[0]
            await first_channel.send("Hello! Thanks for adding me to your server!")

@bot.command
async def set_channel(ctx, channel: discord.TextChannel):
    # Save the channel ID for future use
    with open("channel_config.txt", "w") as f:
        f.write(str(channel.id))
    await ctx.send(f"Channel set to: {channel.name}")

async def post_tue_gifs():
    # Read the saved channel ID
    with open("channel_config.txt", "r") as f:
        channel_id = int(f.read())

    channel = bot.get_channel(channel_id)
    if channel:
        for gif in tuesdayGifs:
            await channel.send(gif)

async def post_wed_gifs():
    # Read the saved channel ID
    with open("channel_config.txt", "r") as f:
        channel_id = int(f.read())

    channel = bot.get_channel(channel_id)
    if channel:
        for gif in wednesdayGifs:
            await channel.send(gif)

@bot.command
async def post_test(ctx):
    # Read the saved channel ID
    with open("channel_config.txt", "r") as f:
        channel_id = int(f.read())

    channel = bot.get_channel(channel_id)
    if channel:
        channel.send("This is a test!")


# Lambda handler function
def lambda_handler(event, context):
    token = os.environ['DISCORD_TOKEN']
    bot.run(TOKEN)