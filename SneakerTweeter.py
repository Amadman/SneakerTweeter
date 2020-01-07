import t
import time
import twitter
import yaml

class SneakerTweeter:
  def __init__(self, sleep=10, config="config/config.yml"):
    self.sleep = sleep
    self.api = twitter.Api(
      t.CONSUMER_KEY, t.CONSUMER_SECRET, t.ACCESS_TOKEN_KEY, t.ACCESS_TOKEN_SECRET
    )

    try:
      self.config = yaml.safe_load(open(config))
    except:
      raise

    self.user = self.config.get('user')
    self.subscriptions = self.config.get('subscriptions')

  def run(self):
    latest_tweet = None

    while(True):
      timeline = self.api.GetUserTimeline(
        screen_name='SneakerDealsGB',
        since_id=latest_tweet,
        count=10,
        trim_user=True,
        exclude_replies=True,
      )

      if len(timeline) > 0:
        latest_tweet = timeline[0].id

        text = "I found the shoe(s) you were looking for!\n"
        for tweet in timeline:
          link = f"https://twitter.com/i/web/status/{tweet.id_str}"
          text += f"{link}\n"

        print(f"Found {len(timeline)} matching tweets")

        self.api.PostDirectMessage(text, screen_name=self.user)
        print(f"Direct Message sent to {self.user}")
      else:
        print("No tweets found!")
        
      print(f"Sleeping for {self.sleep} seconds...")
      time.sleep(self.sleep)