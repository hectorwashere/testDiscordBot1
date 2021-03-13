#!/usr/bin/env python3
"""
littenbot.py
An example discord bot written to demonstrate how to add a reaction in response to specific commands/keywords from messages.

"""
import discord
import yaml

botConfig=yaml.safe_load(open('config.yml','r'))

helloEmojis='🍕🍓🍇🍏🍪'
startLines=('hello','hi','hai','o hai','ohai',"i'm new",'new here','sup','good morning','good afternoon','good evening','👋')

client=discord.Client()

@client.event
async def on_ready():
    print(f'Bot {client.user} connected ')
    guild=discord.utils.find(lambda g: g.id == botConfig['discordGuildID'], client.guilds)
    print(f'Guild set: {guild.name} (ID {guild.id})')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    print(f'{message.author} sent message: {message.content}')
    if message.content in ('!hello','!newhere') or await doStartLinesMatch(message.content,startLines):
        #await message.channel.send('Hai!')
        for emoji in helloEmojis:
            await message.add_reaction(emoji)

async def doStartLinesMatch(messageContent,startLines):
    for startLine in startLines:
        if messageContent.lower().startswith(startLine):
            return True
    return False

client.run(botConfig['discordToken'])
