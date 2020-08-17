import os
import discord
import t
import twitter
import yaml
from dotenv import load_dotenv
from discord.ext import commands, tasks

load_dotenv()
token = os.getenv('DISCORD_TOKEN')
client = discord.Client()

subscription = []
@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')
  sub.start()

@tasks.loop(seconds=10)
async def sub():
  channel = client.get_channel(470595825584832512)
  api = twitter.Api(
    t.CONSUMER_KEY, t.CONSUMER_SECRET, t.ACCESS_TOKEN_KEY, t.ACCESS_TOKEN_SECRET
  )

  timeline = api.GetUserTimeline(
    screen_name='SneakerDealsGB',
    count=10,
    trim_user=True,
    exclude_replies=True,         
  ) 

  for tweet in timeline:
    for x in subscription:
      if x in tweet.text:
        await channel.send(tweet.text)

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
      count=1,
      trim_user=True,
      exclude_replies=True,
    )
    
    if len(timeline) > 0:
      latest_tweet = timeline[0]
      await message.channel.send(latest_tweet.text)

  if message.content.startswith('!sub'):
    api = twitter.Api(
      t.CONSUMER_KEY, t.CONSUMER_SECRET, t.ACCESS_TOKEN_KEY, t.ACCESS_TOKEN_SECRET
    )

    timeline = api.GetUserTimeline(
      screen_name='SneakerDealsGB',
      count=10,
      trim_user=True,
      exclude_replies=True,
    ) 

    for tweet in timeline:
      for x in subscription:
        if x in tweet.text:
          await message.channel.send(tweet.text)

  if message.content.startswith('!new'):
    subscription.append(message.content[4:])
    await message.channel.send(message.content[4:] + ' has been added to subscriptions')
    
client.run(token)       