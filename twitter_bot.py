import tweepy
from TwitterBotPackage import constants


class FavRetweetListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print("Processing tweet id: ", tweet.id)
        if not tweet.favorited:
            # Attempt to favorite tweet
            try:
                tweet.favorite()
            except Exception as e:
                print("Error: could not favorite tweet")
        if not tweet.retweeted:
            # Attempt to retweet tweet
            try:
                tweet.retweet()
            except Exception as e:
                print("Error: Could not retweet tweet")
        self.api.update_status(
            # Need to randomly select status from dict
            # or have different replies for different users
            status="Good Tweet",
            in_reply_to_status_id=tweet.id,
            auto_populate_reply_metadata=True
        )

    def on_error(self, status):
        print("Status: ", status)


def create_api():
    auth = tweepy.OAuthHandler(constants.keys['consumer_key'], constants.keys['consumer_secret'])
    auth.set_access_token(constants.keys['access_token'], constants.keys['access_token_secret'])
    api = tweepy.API(auth)
    return api


def main():
    api = create_api()
    tweets_listener = FavRetweetListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    # Use dict for follow IDs, move to separate file
    stream.filter(follow=constants.ids)
    # Stop program on keyboard interrupt


if __name__ == "__main__":
    main()

# Need to add follow followers function,
# which may be difficult because it is a locked account
# Add to FavRetweetListener, which should be renamed to StreamListener
