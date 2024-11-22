import sqlite3


# function to add birth dates to users
def add_birth_dates():
    birth_dates = ['10/18/1999', '8/19/1998', '9/29/2001', '11/26/1995',
                   '10/22/2002', '12/22/1999', '10/5/2000', '1/3/2003']

    connection = sqlite3.connect('social_media.db')
    cursor = connection.cursor()

    # add birthday column
    cursor.execute('ALTER TABLE users ADD COLUMN birth_date TEXT')

    # loop to add user birth dates
    for user_id, birth_date in enumerate(birth_dates, start=1):
        cursor.execute("UPDATE users SET birth_date = ? WHERE user_id = ?", (birth_date, user_id))

    # commit and close connection
    connection.commit()
    connection.close()
    print("Birth dates added successfully.")
