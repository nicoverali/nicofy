import psycopg2

def connect():
    database = psycopg2.connect('dbname=nicofy user=postgres password=admin')
    cursor = database.cursor()
    return database , cursor

def check_For_User(user):
    DB, cursor = connect()
    cursor.execute('SELECT user_id FROM users WHERE user_id = %s',(user,))
    result = cursor.fetchall()
    DB.close()
    if len(result) == 0:
        return False
    return True

def check_For_Existing_Link(url):
    DB, cursor = connect()
    cursor.execute('SELECT new_link FROM links WHERE new_link = %s',(url,))
    result = cursor.fetchall()
    DB.close()
    if len(result) == 0:
        return False
    return True

def add_User(user):
    DB, cursor = connect()
    cursor.execute('INSERT INTO users VALUES(%s, DEFAULT)',(user,))
    DB.commit()
    DB.close()

def add_Link(old_Link, new_Link, user):
    if not(check_For_User(user)):
        add_User(user)
    DB, cursor = connect()
    cursor.execute('INSERT INTO links VALUES(DEFAULT, %s, %s, %s, DEFAULT)',(new_Link,old_Link,user))
    DB.commit()
    DB.close()

def get_Redirect_Link(new_Link):
    DB, cursor = connect()
    cursor.execute('SELECT old_link FROM links WHERE new_link = %s',(new_Link,))
    result = cursor.fetchall()
    if len(result) == 0:
        raise LookupError("Link doesn't exist")
    return result[0][0]
