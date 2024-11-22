import sqlite3
import pwinput
import datetime

from csv_to_sqlite import load_csv_to_sqlite
from birth_date import add_birth_dates

# user login function to authenticate the user
def user_login():
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()

    while True:
        username = input("Enter username: ")
        # use pwinput to hide the password
        password = pwinput.pwinput(prompt="Enter password: ")

        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()

        if result:
            if result[0] == password:
                print("Login successful!")
                return username
            else:
                print("Access denied. Incorrect password.")
        else:
            print("User not found.")

# view user info function to show user information
def view_user_info(username):
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_info = cursor.fetchone()
    print(f"Username: {user_info[2]}")
    print(f"First Name: {user_info[5]}")
    print(f"Last Name: {user_info[6]}")
    print(f"Email: {user_info[1]}")
    print(f"Birth Date: {user_info[7]}")
    print(f"Account Created Date: {user_info[4]}")

# update user info function to update user information
def update_user_info(username):
    # show all available columns to edit, prompt which column to edit, then update the value
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user_info = cursor.fetchone()
    print("Available columns to update:")
    print("email_id")
    print("password")
    print("first_name")
    print("last_name")
    print("birth_date")

    # include handling for if they enter a column that doesn't exist
    column = input("Enter the column you want to update: ")
    while column not in ["email_id", "password", "first_name", "last_name", "birth_date"]:
        print("Invalid column name. Please try again.")
        column = input("Enter the column you want to update: ")

    new_value = input(f"Enter the new value for {column}: ")

    query = f"UPDATE users SET {column} = ? WHERE username = ?"
    cursor.execute(query, (new_value, username))
    conn.commit()
    print("User info updated successfully.")

# view posts function to show all posts by the user
def view_posts(username):
    # join posts and users tables on user_id, only show the posts that belong to the user_id of the user
    cursor.execute("SELECT post, posted_date FROM posts p INNER JOIN users u"
                   " ON u.user_id=p.user_id WHERE username = ?", (username,))
    posts = cursor.fetchall()
    for post in posts:
        print(f"Post: {post[0]}")
        print(f"Posted Date: {post[1]}")
        print("-------")

# create post function to insert a new post into the posts table
def create_post(username):
    post = input("Enter your post: ")
    posted_date = datetime.datetime.now().strftime("%m/%d/%Y")

    # Retrieve user_id based on username
    cursor.execute("SELECT user_id FROM users WHERE username = ?", (username,))
    user_id = cursor.fetchone()[0]

    # Insert the post with the user_id
    cursor.execute("INSERT INTO posts (user_id, post, posted_date) VALUES (?, ?, ?)", (user_id, post, posted_date))
    conn.commit()
    print("Post created successfully.")

# list followers function to list all followers and who the user is following
def list_followers(username):
    cursor.execute("SELECT u.username FROM users u "
                   "INNER JOIN followers f ON u.user_id = f.follow_id "
                   "WHERE f.user_id = (SELECT user_id FROM users WHERE username = ?)", (username,))
    followers = cursor.fetchall()
    print(f"Followers:")
    for follower in followers:
        print(f"{follower[0]}")

    print(f"-------")
    # also list who the user is following
    cursor.execute("SELECT u.username FROM users u "
                   "INNER JOIN followers f ON u.user_id = f.user_id "
                   "WHERE f.follow_id = (SELECT user_id FROM users WHERE username = ?)", (username,))
    following = cursor.fetchall()
    print(f"Following:")
    for follow in following:
        print(f"{follow[0]}")

# logout function to close the connection
def logout():
    print("Logged out successfully.")
    conn.close()

# main function to run the program
def main():
    username = user_login()
    if username:
        while True:
            print("\nOptions:")
            print("1. View User Info")
            print("2. Update User Info")
            print("3. View Your Posts")
            print("4. Create a New Post")
            print("5. List Followers")
            print("6. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                view_user_info(username)
            elif choice == "2":
                update_user_info(username)
            elif choice == "3":
                view_posts(username)
            elif choice == "4":
                create_post(username)
            elif choice == "5":
                list_followers(username)
            elif choice == "6":
                logout()
                break
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    load_csv_to_sqlite()
    add_birth_dates()
    conn = sqlite3.connect('social_media.db')
    cursor = conn.cursor()
    main()
