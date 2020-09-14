from piazza_api import Piazza
from piazza_object.piazza_object import PiazzaObject
import numpy as np
from discord import Client, Embed, TextChannel
from discord.ext import tasks
from datetime import datetime
import html

global sent_ids
sent_ids = []
token = 'token'
channel_id = 0
client = Client()

@client.event
async def on_message(message):
    print('on_message')
    if message.content == '!ping':
        await message.channel.send(f'{message.author.mention} , pong')

    if message.content == '!piazzacheck':
        new_posts_loop.restart()

    if message.content == '!topbruhmoment':
        if message.channel.id == channel_id:
            await message.channel.send(embed=Embed(title="here", url="https://www.youtube.com/watch?v=dQw4w9WgXcQ"))

@client.event
async def on_ready():
    new_posts_loop.start()

@tasks.loop(minutes=30)
async def new_posts_loop():
    await send_new_posts()

async def send_new_posts():
    load_sent_ids()
    print('\n\nloaded')
    print(sent_ids)
    print('\n\n')

    p = Piazza()
    p.user_login("email", "pass")

    user_status = p.get_user_status()
    nid = user_status['networks'][0]['id']

    eecs2030 = p.network(nid)
    feed = eecs2030.get_feed(limit=99999)

    feed_arr = feed['feed'];
    piazzaobj_arr = []

    for post in feed_arr:
        full_post = eecs2030.get_post(post['id'])
        latest_update = full_post['history'][0]
        piazzaobj_arr.append(
            PiazzaObject(
                post['id'],
                latest_update['subject'],
                latest_update['content'],
                full_post['created'],
                'https://piazza.com/class?cid=' + post['id']
                )
            )

    print(sent_ids)
    for piazzaobj in piazzaobj_arr:
        if not piazzaobj.id in sent_ids:
            print(f'sending {piazzaobj.id}')
            await send_post(piazzaobj)
            sent_ids.append(piazzaobj.id)

    save_sent_ids()

def load_sent_ids():
    global sent_ids
    sent_ids = np.loadtxt('sent_ids.txt', dtype=str).tolist()

async def send_post(piazzaobj):
    embed = Embed(
        title=format(piazzaobj.subject),
        url=piazzaobj.link,
        description=format(piazzaobj.content),
        color=0x2e6f9e,
        timestamp=datetime.strptime(piazzaobj.date, "%Y-%m-%dT%H:%M:%SZ")
        )
    embed.set_thumbnail(url="https://miro.medium.com/fit/c/336/336/0*JujCDaEQ-prYBaEZ.png")
    channel = client.get_channel(channel_id)
    await channel.send(embed=embed)

def save_sent_ids():
    f = open('sent_ids.txt', 'w')
    np.savetxt('sent_ids.txt', sent_ids, fmt='%s')

def format(text):
    """Remove html tags from a string"""
    import re
    clean = re.compile('<.*?>')
    cleantext = re.sub(clean, '', text)
    return html.unescape(cleantext)

client.run(token)