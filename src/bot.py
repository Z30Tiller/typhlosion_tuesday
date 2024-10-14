import os
import discord
import datetime

from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.guilds = True
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# List of Tuesday GIF URLs
tuesdayGifs = [
    # 'https://tenor.com/en-GB/view/typhlosion-tuesday-meme-gif-5109207821042719955',
    # 'https://tenor.com/en-GB/view/typhlosion-tuesday-meme-tuesday-poke-meme-gif-26753999',
    # 'https://tenor.com/en-GB/view/happy-typhlosion-tuesday-meme-gif-4051929047719001080'
    'https://tenor.com/f65s0hvL6sb.gif',
    'https://tenor.com/lGz2TvweQGd.gif',
    'https://tenor.com/nmnVg5vG8Nr.gif'
]

# List of Wednesday GIF URLs
wednesdayGifs = [
    # 'https://tenor.com/en-GB/view/pokemon-typhlosion-tuesday-gif-12713113255833901878'
    'https://tenor.com/bTpgt.gif',
    'https://tenor.com/w0Xh.gif'
]

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    # Get the current date
    today = datetime.datetime.now()

    # Get the day of the week (Monday is 0 and Sunday is 6)
    day_of_week = today.weekday()

    # Read the channel_id
    channel_id = int(os.environ['CHANNEL_ID'])
    channel = bot.get_channel(channel_id)

    print(f'Day of the week is {day_of_week}')
    print(f'Channel is {channel}')

    if channel:
        if day_of_week == 1:
            for gif in tuesdayGifs:
                await channel.send(gif)
        elif day_of_week == 2:
            for gif in wednesdayGifs:
                await channel.send(gif)
        else:
            print(f'Day of the week does not match')
    else:
        print(f'Channel not loaded correctly')

# @bot.event
# async def on_guild_join(guild):
#     # This event is triggered when the bot joins a new server
#     print(f"Bot added to server: {guild.name} (ID: {guild.id})")

#     # You can choose a default channel to send a message to or configure further
#     # Generally, try to find the 'general' text channel or the first channel
#     for channel in guild.text_channels:
#         if "general" in channel.name:
#             await channel.send("Hello! Thanks for adding me to your server!")
#             break
#         else:
#             # Fallback to the first available text channel
#             first_channel = guild.text_channels[0]
#             await first_channel.send("Hello! Thanks for adding me to your server!")

# @bot.command
# async def set_channel(ctx, channel: discord.TextChannel):
#     # Save the channel ID for future use
#     with open("channel_config.txt", "w") as f:
#         f.write(str(channel.id))
#     await ctx.send(f"Channel set to: {channel.name}")

# Lambda handler function
def lambda_handler(event, context):
    token = os.environ['DISCORD_TOKEN']
    bot.run(TOKEN)

# bot.run(os.environ['DISCORD_TOKEN'])