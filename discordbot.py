#!/usr/bin/env python3
import os
import discord
import yaml

botConfig=yaml.safe_load(open('config.yml','r'))
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
    helloEmojis='🍕🍓🍇🍏🍪'
    startLines=('hello','hi','hai','o hai','ohai',"i'm new",'new here','sup')
    #TODO: Too many lines here. I'll fix this later.
    if message.content in ('!hello','!newhere') or\
    await doStartLinesMatch(message.content,startLines):
        #await message.channel.send('Hai!')
        for emoji in helloEmojis:
            await message.add_reaction(emoji)

async def doStartLinesMatch(messageContent,startLines):
    for startLine in startLines:
        if messageContent[0:len(startLine)].lower() == startLine:
            return True
    return False
client.run(botConfig['discordToken'])