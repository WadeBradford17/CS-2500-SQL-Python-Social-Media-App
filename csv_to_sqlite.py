import sqlite3
import pandas as pd

# function to load csv data into sqlite
def load_csv_to_sqlite():
    connection = sqlite3.connect('social_media.db')

    # load csv files
    users_df = pd.read_csv('users.csv')
    followers_df = pd.read_csv('followers.csv')
    posts_df = pd.read_csv('posts.csv')

    # create tables
    users_df.to_sql('users', connection, if_exists='replace', index=False)
    followers_df.to_sql('followers', connection, if_exists='replace', index=False)
    posts_df.to_sql('posts', connection, if_exists='replace', index=False)

    # commit and close connection
    connection.commit()
    connection.close()
    print("Data loaded successfully into social_media.db")
