#!/usr/bin/env python3
"""
littenbot.py
An example discord bot written to demonstrate how to add a reaction in response to specific commands/keywords from messages.

"""
import discord
import os
try:
    import yaml
except ModuleNotFoundError:
    print('PyYAML not installed. Install PyYAML and then try again.')
    exit()

try:
    botConfig=yaml.safe_load(open('config.yml','r'))
except IOError as loadFailureObject:
    if (loadFailureObject.args[0] == 2):
        print('config.yml does not exist. Rename config.yml.example to config.yml and then try again.')
    else:
        print('Failed to load config.yml: {loadFailureObject}'.format(loadFailureObject))
    exit()

try:
    if 'discordToken' not in botConfig:
        botConfig['discordToken']=os.environ['DISCORDTOKEN']
except KeyError:
    print("discordToken not defined in config.yml")
    print("Tried to use environment variable DISCORDTOKEN instead, but it doesn't exist.")
    print("Exiting...")
    exit()



client=discord.Client()

@client.event
async def on_ready():
    print(f'Bot {client.user} connected ')
    for guild in client.guilds:
        print(f'Connected to Discord Server: {guild.name} (ID {guild.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f'{message.author} sent message: {message.content}')
    if message.content in ('!hello','!newhere') or await isPrefixMatch(message.content,botConfig['linePrefixes']):
        for emoji in botConfig['helloEmojis']:
            await message.add_reaction(emoji)

async def isPrefixMatch(messageContent,linePrefixes):
    for linePrefix in linePrefixes:
        if messageContent.lower().startswith(linePrefix):
            return True
    return False

client.run(botConfig['discordToken'])
