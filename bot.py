import os
import discord
import asyncio
import time
import aioschedule as schedule
from dotenv import load_dotenv


# Import config file.
#import config
import testconfig as config

# Load our environment variables
load_dotenv()

client = discord.Client()

# Starting message when coming online. Lists bot name and servers it is on.
@client.event
async def on_ready():
    print('Connected as {0.user} on these servers: '.format(client))
    for g in client.guilds:
        print(' - ' + g.name)
    print('+--------------------------------------------------+')

    await client.change_presence(activity=discord.CustomActivity("Studying #the-bible-of-evan"))

    await praise_schedule(config.TIME_INT)
    return


# Action to take when a message is received.
@client.event
async def on_message(message):

    # Correct channel, correct command prefix, not from this bot.
    if message.channel.id == config.COMMAND_CHANNEL and message.content[0] == "&" and message.author != client.user:

        # Will add command functionality later once basics of bot are created.

        # Log received command in console.
        print('Received command \"'
                + message.content[1:]
                + '\" in \"#'
                + message.channel.name
                + '\" on server \"'
                + message.guild.name
                + '\"')

        # If requested command is &pong, send "pong".
        if message.content[1:].lower() == "ping":
            await message.channel.send("Pong!")
            return

        if message.content[1:].lower() == "pong":
            await message.channel.send("That's my part " + message.author.mention + " :(")
            return

        # If requested command is &info, respond with info.
        if message.content[1:].lower() == "info":
            await message.channel.send("```I am a bot that praises Evan 3 times a day!"
                                        + "\nCommands:"
                                        + "\n&info"
                                        + "\n&ping"
                                        + "\n&pong```")
            return

    # If message does not meet requirements to execute, return.
    return

# Praise Evan
async def praise_schedule(time_interval):

    # Schedule to run 3 times a day.
    # Adjusted UTC times so that this occurs at 00:00, 08:00, 16:00 PST. Will
    # fix this so it adjusts timezone auto
    schedule.every().day.at("7:00").do(lambda: praise(''))
    schedule.every().day.at("15:00").do(lambda: praise(''))
    schedule.every().day.at("23:00").do(lambda: praise(''))

    # Testing case
    #schedule.every(3).seconds.do(lambda: praise(''))

    # Check for tasks to run every 'time_interval' seconds.
    while True:
        local_t = time.localtime()
        print("Checking for a scheduled task to execute ("
                + str(local_t.tm_hour).zfill(2)
                + ":"
                + str(local_t.tm_min).zfill(2)
                + ":"
                + str(local_t.tm_sec).zfill(2)
                + ")")

        await schedule.run_pending()
        await asyncio.sleep(time_interval)


# Praise Evan :D
async def praise(sermon):
    channel = client.get_channel(config.BROADCAST_CHANNEL)
    if sermon != '':
        await channel.send(sermon)
    await channel.send("!praise be")


# Get the token and run bot.
def run():
    #with open('token', "r") as token_f:
    #    token = token_f.read()
    client.run(os.getenv("DISCORD_TOKEN"))

# Run the bot client.
run()
