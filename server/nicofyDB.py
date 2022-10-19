import MySQLdb
import psycopg2
import os
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

db = urlparse(os.getenv("DATABASE_URL"))
links_table = os.getenv("DB_TABLE_LINKS")
users_table = os.getenv("DB_TABLE_USERS")


def connect():
    database = MySQLdb.connect(
        host=db.hostname,
        user=db.username,
        passwd=db.password,
        db=db.path[1:],
    )
    cursor = database.cursor()
    return database, cursor


def check_For_User(user):
    DB, cursor = connect()
    cursor.execute('SELECT user_id FROM '+users_table+' WHERE user_id = %s',
                   (user,))
    result = cursor.fetchall()
    DB.close()
    if len(result) == 0:
        return False
    return True


def check_For_Existing_Link(url):
    DB, cursor = connect()
    cursor.execute('SELECT new_link FROM '+links_table+' WHERE new_link = %s',
                   (url,))
    result = cursor.fetchall()
    DB.close()
    if len(result) == 0:
        return False
    return True


def add_User(user):
    DB, cursor = connect()
    cursor.execute('INSERT INTO '+users_table+' VALUES(%s)', (user,))
    DB.commit()
    DB.close()


def add_Link(old_Link, new_Link, user):
    if not (check_For_User(user)):
        add_User(user)
    DB, cursor = connect()
    cursor.execute(
        'INSERT INTO '+links_table+' VALUES(DEFAULT, %s, %s, %s)', (new_Link, old_Link, user))
    DB.commit()
    DB.close()


def get_Redirect_Link(new_Link):
    DB, cursor = connect()
    cursor.execute(
        'SELECT old_link FROM '+links_table+' WHERE new_link = %s', (new_Link,))
    result = cursor.fetchall()
    if len(result) == 0:
        raise LookupError("Link doesn't exist")
    return result[0][0]
