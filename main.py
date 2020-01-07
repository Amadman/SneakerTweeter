from SneakerTweeter import SneakerTweeter

if __name__ == "__main__":
  try:
    tweeter = SneakerTweeter(sleep=2, config="config/config.yml")
    tweeter.run()
  except Exception as e:
    raise