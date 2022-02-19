from utils import get_config, open_database

import tweepy

def request_tweets(config: dict, max_results: int = 100, limit: int = 2000) -> list:
    client = tweepy.Client(
        bearer_token=config['TWITTER']['BearerToken'],
        wait_on_rate_limit=True)

    tweets = []
    for tweet in tweepy.Paginator(
            client.search_recent_tweets,
            # TODO: Do we want to filter out retweets ? If so, ask for a higher permission to Twitter and use -filter:retweets ?
            query='#{}'.format(config['TWITTER']['Hashtag']),
            expansions='attachments.media_keys',
            tweet_fields=['id', 'text', 'public_metrics'],
            media_fields=['media_key', 'public_metrics'],
            max_results=max_results).flatten(limit=limit):
        d = {}
        d['id'] = tweet.id
        d['text'] = tweet.text.replace("'", '')
        d['retweet_count'] = tweet.public_metrics['retweet_count']
        d['like_count'] = tweet.public_metrics['like_count']
        d['reply_count'] = tweet.public_metrics['reply_count']
        d['view_count'] = tweet.public_metrics['view_count'] if 'view_count' in tweet.public_metrics.keys() else 0
        tweets.append(d)

    return tweets


def create_table_if_not_exists(cur):
    cur.execute("""
    CREATE TABLE IF NOT EXISTS tweets(
      id            VARCHAR(64)  NOT NULL PRIMARY KEY,
      text          VARCHAR(560) NOT NULL,
      like_count    INT          NOT NULL DEFAULT 0,
      retweet_count INT          NOT NULL DEFAULT 0,
      reply_count   INT          NOT NULL DEFAULT 0,
      view_count    INT          NOT NULL DEFAULT 0
      );""")


def main(config):
    conn = open_database(config)
    cur = conn.cursor()
    create_table_if_not_exists(cur)
    tweets = request_tweets(config)

    # Build a single insert request for this batch (it either add new rows or update existing ones)
    insert_sql = "INSERT INTO tweets (id, text, retweet_count, like_count, reply_count, view_count) VALUES ('{}','{}',{},{},{},{})".format(
        tweets[0]['id'], tweets[0]['text'], tweets[0]['retweet_count'], tweets[0]['like_count'], tweets[0]['reply_count'], tweets[0]['view_count'])
    for tweet in tweets[1:]:
        insert_sql = insert_sql + ",('{}','{}',{},{},{},{})".format(
            tweet['id'], tweet['text'], tweet['retweet_count'], tweet['like_count'], tweet['reply_count'], tweet['view_count'])
    insert_sql = insert_sql + \
        'ON DUPLICATE KEY UPDATE text=values(text),retweet_count=values(retweet_count),like_count=values(like_count), reply_count=values(reply_count), view_count=values(view_count);'

    # Execute, flush, close all.
    cur.execute(insert_sql)
    conn.commit()
    cur.close()
    conn.close()


if __name__ == '__main__':
    config = get_config()
    main(config)
