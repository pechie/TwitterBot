import tweepy
import time
from TwitterBotPackage import constants


class StreamListener(tweepy.StreamListener):
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


def check_mentions(api, since_id):
    print("Checking Mentions")
    new_since_id = since_id
    for tweet in tweepy.Cursor(api.mentions_timeline,
                               since_id=since_id).items():
        new_since_id = max(tweet.id, new_since_id)
        if tweet.in_reply_to_status_id is not None:
            print("Answering to ", tweet.user.name)
            api.update_status(
                # Update to say random status from dict
                status="Bold and Brash",
                in_reply_to_status_id=tweet.id,
            )
    return new_since_id


def main():
    api = create_api()
    tweets_listener = StreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(follow=constants.ids)

    since_id = 1
    while True:
        since_id = check_mentions(api, since_id)
        print("Waiting...")
        time.sleep(10)
    # Stop program on keyboard interrupt


if __name__ == "__main__":
    main()

# Need to add follow followers function,
# which may be difficult because it is a locked account
# Add to FavRetweetListener, which should be renamed to StreamListener
# Reply to mentions with either "Bold and Brash" or "Belongs in the trash"
