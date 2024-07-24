import sqlite3
from sqlite3 import Error


def create_table():
    try:
        connection= sqlite3.connect('sqlite3.db')

        table = """ CREATE TABLE Users (
                    user_id BIGINT NOT NULL ,
                    chat_id BIGINT NOT NULL ,
                    message_id BIGINT NOT NULL,
                    click TEXT NOT NULL 
                ); """
        cursor = connection.cursor()
        print("databaza yaratildi")
        cursor.execute(table)
        cursor.close()
    
    except Error as error:
        print("hatolik", error)
    finally:
        if connection:
            connection.close()    
            print("sqlite o'chdi")
# create_table()
            

def Add_db(chat_id, message_id, like, dislike):
    try:
        with sqlite3.connect("sqlite3.db") as connection:
            cursor = connection.cursor()
            
            table = '''
                INSERT INTO Posts(chat_id, message_id, like, dislike) VALUES( ?, ?, ?, ?)
            '''
            cursor.execute(table, (chat_id, message_id, like, dislike))
            connection.commit()
            print("Post tablega qo'shildi")
            cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if connection:
            connection.close()
            # print("Sqlite ish foalyatini tugatdi")                


def AddUser(user_id ,chat_id, message_id, click):
    try:
        with sqlite3.connect("sqlite3.db") as connection:
            cursor = connection.cursor()
            
            table = '''
                INSERT INTO Users(user_id ,chat_id, message_id, click) VALUES( ?, ?, ?, ?)
            '''
            cursor.execute(table, (user_id ,chat_id, message_id, click))
            connection.commit()
            print("User tablega qo'shildi")
            cursor.close()

    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if connection:
            connection.close()
            # print("Sqlite ish foalyatini tugatdi")   
# AddUser(123, 456, 789, 'like')             


def Read_db():
    try:
        with sqlite3.connect("sqlite3.db") as sqliteconnection:
            cursor = sqliteconnection.cursor()
            sql_query = """
                SELECT * FROM Posts 
            """
        
            cursor.execute(sql_query) 
            A = cursor.fetchall()
            print("Posts table oqildi")
            return A

    except Error as error:
        print("xatolik:", error)
    finally:
        if sqliteconnection:
            sqliteconnection.close()
            # print("sqlite faoliyatini tugatdi")


def ReadUser():
    try:
        with sqlite3.connect("sqlite3.db") as sqliteconnection:
            cursor = sqliteconnection.cursor()
            sql_query = """
                SELECT * FROM Users 
            """
        
            cursor.execute(sql_query) 
            A = cursor.fetchall()
            print("User table oqildi")
            return A

    except Error as error:
        print("xatolik:", error)
    finally:
        if sqliteconnection:
            sqliteconnection.close()
            # print("sqlite faoliyatini tugatdi")


def UpdateLike(like, chat_id, message_id):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE Posts SET like = ? WHERE (chat_id, message_id) = (?, ?)", (like, chat_id, message_id)
            )
            con.commit()
            print("like soni yangilandi")
            cur.close()

    except sqlite3.Error as err:
        print(f"Yangilashda xatolik: {err}")
    finally:
        if con:
            con.close()
            # print("Sqlite ish foalyatini tugatdi")  


def UpdateDislike(dislike, chat_id, message_id):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE Posts SET dislike = ? WHERE (chat_id, message_id) = (?, ?)", (dislike, chat_id, message_id)
            )
            con.commit()
            print("dislike soni yangilandi")
            cur.close()

    except sqlite3.Error as err:
        print(f"Yangilashda xatolik: {err}")
    finally:
        if con:
            con.close()
            # print("Sqlite ish foalyatini tugatdi")  


def UpdateUser(user_id ,chat_id, message_id, click):
    try:
        with sqlite3.connect("sqlite3.db") as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE Posts SET click = ? WHERE (user_id, chat_id, message_id) = (?, ?, ?)", (click, user_id ,chat_id, message_id)
            )
            con.commit()
            print("user soni yangilandi")
            cur.close()

    except sqlite3.Error as err:
        print(f"Yangilashda xatolik: {err}")
    finally:
        if con:
            con.close()
            # print("Sqlite ish foalyatini tugatdi")  


def DeleteUser(user_id, chat_id, message_id):
    try:
        connection = sqlite3.connect('sqlite3.db')
        cursor = connection.cursor()

        table = '''
            DELETE FROM Users WHERE (user_id, chat_id, message_id) = (?, ?, ?)
        '''
        cursor.execute(table, (user_id, chat_id, message_id))
        connection.commit()
        print("User tabledan o'chirildi")
        cursor.close()
    
    except sqlite3.Error as error:
        print("Error while creating a sqlite table", error)
    finally:
        if connection:
            connection.close()
            # print("Sqlite ish foalyatini tugatdi")
# DeleteUser(123, 456, 789)