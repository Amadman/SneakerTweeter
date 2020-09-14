import os
import discord
import t
import twitter
import yaml
import sqlite3
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = discord.Client()

@client.event
async def on_ready():
  conn = sqlite3.connect('subscriptions.sqlite')
  c = conn.cursor()
  c.execute('''CREATE TABLE sneakers
             (subscriptions text, userID integer)''')
  conn.commit()
  conn.close()
  print(f'{client.user} has connected to Discord!')
  sub.start()

@tasks.loop(minutes=1)
async def sub():
  channel = client.get_channel(470595825584832512)
  api = twitter.Api(
    t.CONSUMER_KEY, t.CONSUMER_SECRET, t.ACCESS_TOKEN_KEY, t.ACCESS_TOKEN_SECRET
  )

  conn = sqlite3.connect('subscriptions.sqlite')
  c = conn.cursor()
  c.execute(f"SELECT subscriptions FROM sneakers")

  timeline = api.GetUserTimeline(
    screen_name='SneakerDealsGB',
    count=10,
    trim_user=True,
    exclude_replies=True,         
  ) 

  for tweet in timeline:
      for row in c.execute('SELECT * FROM sneakers'):
        if row[0] in tweet.text:
          user = client.get_user(row[1])
          await user.send(tweet.text)
          
  conn.close()        

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if message.content.startswith('!help'):
    await message.channel.send('I am the SneakerHead. Type !help for this help message')
    
  if message.content.startswith('!latest'):
    api = twitter.Api(
     t.CONSUMER_KEY, t.CONSUMER_SECRET, t.ACCESS_TOKEN_KEY, t.ACCESS_TOKEN_SECRET
    )

    timeline = api.GetUserTimeline(
      screen_name='SneakerDealsGB',
      count=10,
      trim_user=True,
      exclude_replies=True,
    )
    
    if len(timeline) > 0:
      latest_tweet = timeline[0]
      await message.channel.send(latest_tweet.text)

  if message.content.startswith('!new'):
    user_id = (message.author.id)
    sneaker = (message.content[4:], user_id)
    await message.channel.send(message.content[4:] + ' has been added to subscriptions')
    conn = sqlite3.connect('subscriptions.sqlite')
    c = conn.cursor()
    c.execute("INSERT INTO sneakers VALUES (?, ?)", sneaker )
    conn.commit()
    conn.close()

client.run(token)       