import discord
import asyncio
import aiohttp
import traceback
import sys
import os
import re
import datetime
import time
from datetime import datetime,tzinfo,timedelta
from random import randint



print ('Logging into Discord...')
activeContest = {}
timer = {}
startdate = {}
# Check if the attachment is a image
r_url = re.compile(r"^http?:")
r_image = re.compile(r".*\.(jpg|png|gif)$")
# The channel ID that participants will submit their image into
submissionChannel = ''
# The channel ID that images will reappear after being deleted from the submission channel
reviewingChannel = ''

client = discord.Client()

def is_bot(m):
    return m.author == client.user



@client.event
async def on_message(message):
    if message.content.lower().startswith('te!'):
        if message.content.lower().startswith('te!startcontest'):
            userstr = message.content
            userstr = userstr.replace('te!startcontest', '')
            userstr = userstr.replace(' ', '')
            if userstr.isdigit():
                startdate[message.channel.id] = time.time()
                timer[message.channel.id] = int(userstr)
                enddate[message.channel.id] = (startdate[message.channel.id] + timer[message.channel.id])
            elif userstr == '':
                pass
            else:
                await client.send_message(message.channel, 'Duration must be in seconds!')
                return
            activeContest[message.channel.id] = True
            await client.delete_message(message)
            await client.send_message(message.channel, 'Now accepting submissions! Upload your screenshot to a place of your choice then link it with the URL and a mention to {}!'.format(client.user.mention))
            
        elif message.content.lower() == 'te!closecontest':
            try:
                del activeContest[message.channel.id]
                await client.purge_from(client.get_channel(reviewingChannel), limit=100)
                await client.delete_message(message)
                await client.send_message(message.channel, 'Submissions are now closed!')
                time.sleep(5)
                await client.purge_from(message.channel, limit=2, check=is_bot)
            except KeyError:
                await client.send_message(message.channel, 'You are either not in the right channel or there was no contest to delete in the first place.')
                
        elif message.content.lower() == 'te!shutdown':
            if message.author.id == '':
                await client.send_message(message.channel, 'DONT DO THIS TO ME MA-')
                await client.logout()
            else:
                await client.send_message(message.channel, 'CANT LET YOU DO THAT, STARFOX.')
                

            
    elif message.content.lower().startswith('{}'.format(client.user.mention)):
        userstr = message.content
        userstr = userstr.replace('{}'.format(client.user.mention), '')
        userstr = userstr.replace(' ', '')
        if message.channel.id == submissionChannel:
            try:
                if activeContest[message.channel.id] == True:
                    if r_image.match(userstr):
                        currentTime = time.strftime('%H:%M:%S')
                        em = discord.Embed(description='', colour=0xB3ECFF)
                        em.add_field(name='Submitter', value='{}'.format(message.author.mention), inline=True)
                        em.add_field(name='Time Submitted', value=str(currentTime), inline=True)
                        em.set_image(url=userstr)
                        em.set_author(name='Submission (In US CST)')
                        await client.send_message(client.get_channel(reviewingChannel), '', embed=em)
                        await client.delete_message(message)
                        #await client.send_message(client.get_channel(reviewingChannel), '**Submission**:\n {} \n'.format(message.author.mention) + imageurl)
                    elif message.embeds != None:
                        try:
                            imageurl = message.embeds[0]['thumbnail']['url']
                            currentTime = time.strftime('%H:%M:%S')
                            em = discord.Embed(description='', colour=0xB3ECFF)
                            em.add_field(name='Submitter', value='{}'.format(message.author.mention), inline=True)
                            em.add_field(name='Time Submitted', value=str(currentTime), inline=True)
                            em.set_image(url=imageurl)
                            em.set_author(name='Submission (In US CST)')
                            await client.send_message(client.get_channel(reviewingChannel), '', embed=em)
                            await client.delete_message(message)
                        except IndexError:
                            await client.send_message(message.channel, 'Your submission must be an image!')
                            await client.delete_message(message)
                    else:
                        await client.send_message(message.channel, 'Submission must be an image!')
                        await client.delete_message(message)
                        return
                else:
                    await client.send_message(message.channel, 'There is no contest going on at this moment!')
            except KeyError:
                await client.send_message(message.channel, 'There is no contest here!')
        else:
            await client.send_message(message.channel, 'You are not in the right channel!')               
                
                
@client.event
async def on_ready():
    print('Logged in as:')
    print(client.user.name)
    print(client.user.id)
    print('Logged into servers:')
    for item in client.servers:
        print (item)
    print ('Tenk is now ready')
    print('------')
    await client.change_presence(game=discord.Game(name='just tenk things'))
    
client.run('key')