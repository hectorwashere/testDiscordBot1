#!/usr/bin/env python3
"""
littenbot.py
An example discord bot written to demonstrate how to add a reaction in response to specific commands/keywords from messages.

"""

import os
try:
    import yaml
    import discord
    from discord.ext import commands
except ModuleNotFoundError:
    print('pyyaml and/or discord.py not installed. Verify that both are installed and then try again.')
    exit()

botConfig={}
try:
    botConfig=yaml.safe_load(open('config.yml','r'))
except IOError as loadFailureObject:
    if (loadFailureObject.args[0] == 2):
        print('config.yml does not exist. Using fallback configuration...')
        botConfig['useMessagePrefixes']=False
    else:
        print(f'Failed to load config.yml: {loadFailureObject}')
        exit()

try:
    if 'discordToken' not in botConfig:
        botConfig['discordToken']=os.environ['DISCORDTOKEN']
except KeyError:
    print("discordToken not defined in config.yml")
    print("Tried to use environment variable DISCORDTOKEN instead, but it doesn't exist.")
    print("Exiting...")
    exit()


bot=commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'Bot {bot.user} connected ')
    for guild in bot.guilds:
        print(f'Connected to Discord Server: {guild.name} (ID {guild.id})')

#Example - Part 1: Add !hello/!newhere command
#Taken in part from https://discordpy.readthedocs.io/en/latest/ext/commands/commands.html
@bot.command(aliases=['newhere'])
async def hello(ctx):
    await addHelloEmojis(ctx.message)


#Part 2: Message prefixes, provided the setting useMessagePrefixes is set to True
@bot.event
async def on_message(message):
    if botConfig['useMessagePrefixes'] and\
    await isPrefixMatch(message.content,botConfig['messagePrefixes']):
        #print(f'Emojis added to message from {message.author}: {message.content}')
        await addHelloEmojis(message)
    #Needed for bot commands to work if on_message is overridden.
    #https://github.com/Rapptz/discord.py/issues/186
    await bot.process_commands(message)

#Part 3: This is where the adding of emoji reactions is done.
async def addHelloEmojis(message):
    for emoji in botConfig['helloEmojis']:
        await message.add_reaction(emoji)
    
#Part 4: This is where the message prefix matching is done.
async def isPrefixMatch(messageContent,messagePrefixes):
    for messagePrefix in messagePrefixes:
        if isinstance(messagePrefix,dict):
            if messagePrefix['applyOnlyIfEntireMessage']:
                if messageContent.lower()==messagePrefix['prefix']:
                    return True
                else:
                    continue
            else:
                messagePrefix=messagePrefix['prefix']
        if messageContent.lower().startswith(messagePrefix):
            return True
    return False

bot.run(botConfig['discordToken'])

