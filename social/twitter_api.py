import tweepy
import os
import os.path
import json

from django.conf import settings


try:
    TWITTER_CRED = json.loads(os.environ['TWITTER_CRED'])
except KeyError:
    # Only for development purpose, for production use environment
    # variables instead
    from .local_settings import SOCIAL
    TWITTER_CRED = SOCIAL['TWITTER_CRED']

consumer_key = TWITTER_CRED['consumer_key']
consumer_secret = TWITTER_CRED['consumer_secret']
access_token = TWITTER_CRED['access_token']
access_token_secret = TWITTER_CRED['access_token_secret']

# OAuth process, using the keys and tokens
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Creation of the actual interface, using authentication
twitter_api = tweepy.API(auth)


def set_status(text, in_reply_to=None, handles_to_tag=[], api=twitter_api):

    tags_string = ''
    for i in handles_to_tag:
        tags_string = '{}@{} '.format(tags_string, i)
    try:
        s = api.update_status('{}\n{}'.format(tags_string, text),
                              in_reply_to)
    except tweepy.error.TweepError:
        return None
    return s.id


if (settings.TESTING):
    def set_status(text, in_reply_to=None, handles_to_tag=[], api=twitter_api):
        return '1234'
