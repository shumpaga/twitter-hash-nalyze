# twitter-hash-nalyze

Track specific hashtag in Twitter and do analysis on the tweets.

## Run Example

### MariadDB Database
Make sure you have a running maria db database. If not start it using :
```
systemctl start mariadb
```
Create a database and a user.

### Twitter API
Create a new app in the developers portal and get the [Bearer Token](https://developer.twitter.com/en/docs/authentication/overview).

### Configuration
Using all previous information, set your own `./config.ini` file. Set the hashtag you want to follow.
```
[DATABASE]
User=
Host=
DatabaseName=
Port=
Password=

[TWITTER]
Hashtag=
BearerToken=
```

### Extract Data
Schedule the `./backend/update_data_job.py` job using crontab.

### Visualize Data
Run the frontend using :
```
cd client && npm intall && npm start
```
This frontend lacks of features. It just displays the data without any optimization or advanced analyzis in mind.
