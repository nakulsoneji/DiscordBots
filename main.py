import discord
from discord.ext import commands, tasks
from discord import client
from discord import FFmpegPCMAudio
import random
from random import choice
from datetime import datetime
import time
import requests
from youtube_dl import YoutubeDL
import os

tokens = {"name" : "token}
token = ""

whichbot = input("what bot do you want to use?\n")

for key in tokens:
    if whichbot.lower() == key:
        token = tokens[key]

status = ["gaming", "ur mom", "vibing", "french > spanish", "bing chilling"]
bot = commands.Bot(command_prefix='.')

now = datetime.now()
time = now.strftime("%d/%m/%Y %H:%M:%S")

notsusjokes = dict()

with open("deeznuts.csv") as file:
    for line in file:
        line = line.strip('\n')
        (key, val) = line.split(",")
        notsusjokes[key] = val


@bot.event
async def on_ready():
    change_status.start()
    print("gamers ready, logged on as {0.user}".format(bot))


@bot.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    messages = f'{time}\n(#{channel}) {username}: {user_message}\n'

    with open("logs.txt", "a") as logs:
        logs.write(messages + "\n")

    with open("logs.txt", "r") as logs:
        nonempty_lines = []
        for lines in logs.readlines():
            if lines != "\n":
                nonempty_lines.append(lines)
        line_count = len(nonempty_lines)

    if line_count > 100:
        with open("logs.txt", "r+") as logs:
            logs.truncate(0)

    if message.author == bot.user:
        return

    else:
        user_message_list = user_message.lower().split(" ")
        for words in user_message_list:
            for keys in notsusjokes:
                stripped_word = words.strip("!@#$%^&*()?.,+=_-{}[]|")
                if stripped_word == keys:
                    await message.channel.send(notsusjokes[keys])
                    return
                elif user_message.lower() == keys:
                    await message.channel.send(notsusjokes[keys])
                    return

    if user_message.lower() == "!anywhere":
        await message.channel.send("this can be used anywhere")
        return

    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    username = str(message.author).split("#")[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    shamechannel = discord.utils.get(bot.get_all_channels(), name="wall-of-shame")
    msg = f"{username} deleted message at {time} in {channel}:\n{user_message}\n\n"

    if shamechannel is None:
        await message.channel.send(msg)
    else:
        await shamechannel.send(msg)
    with open("wall_of_shame.txt", "a") as shame:
        shame.write(msg)


@bot.command(help="this command returns the latency")
async def ping(ctx):
    await ctx.send(f"Pong! {round(bot.latency * 1000)}ms")


@bot.command(help="gives the last deleted message")
async def hall_of_shame(ctx):
    with open("wall_of_shame.txt", "r") as shame_text:
        lines = shame_text.readlines()
        last_deleted = []
        the_lines = lines[:-1]

        for n in range(len(the_lines) - 1, -1, -1):
            if the_lines[n] != "\n":
                last_deleted.insert(-1, the_lines[n])
            elif the_lines[n] == "\n" and n != len(the_lines) - 1:
                break

        last_lines_fixed = "".join(last_deleted)
        await ctx.send(f'The currently featured message is: \n{last_lines_fixed}')


# @bot.command(help="bans target user")
# async def spam(ctx, username):
#     for spams in range(10):
#         await ctx.send(username)


@tasks.loop(seconds=20)
async def change_status():
    await bot.change_presence(activity=discord.Game(choice(status)))

bot.run(token)
