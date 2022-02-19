from enum import Enum
from typing import Dict
from flask import Flask
from utils import get_config, open_database

app = Flask(__name__)
config = {}


@app.route("/tweets")
def tweetsHome():
    conn = open_database(config)
    cur = conn.cursor()
    # TODO: Explore Pagination and optimization using https://mariadb.com/kb/en/pagination-optimization/
    cur.execute('SELECT * FROM tweets;')
    raw_tweets = cur.fetchall()
    field_names = [i[0] for i in cur.description]
    return {'tweets': [{field_names[i]: tweet[i]
                        for i in range(len(field_names))} for tweet in raw_tweets]}


if __name__ == "__main__":
    config = get_config()
    app.run(debug=True)
