from configparser import ConfigParser
from os import getcwd, path

import MySQLdb

def get_config() -> dict:
    config = ConfigParser()
    config.read(path.join(getcwd(),'config.ini'))
    return config

def open_database(config : dict):
    try:
        conn = MySQLdb.connect(
            user=config['DATABASE']['User'],
            password=config['DATABASE']['Password'],
            host=config['DATABASE']['Host'],
            port=int(config['DATABASE']['Port']),
            database=config['DATABASE']['DatabaseName'],
            charset='utf8mb4'
        )
    except MySQLdb.Error as e:
        print(f"Error connecting to Database: {e}")
        exit(1)

    return conn
