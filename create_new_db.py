import sqlite3
from datetime import datetime
def create_new_db(db_name):
    """Sets up tables for new database"""
    
    with sqlite3.connect(db_name) as db:
        cursor = db.cursor()

        #create tasks table
        cursor.execute("""CREATE TABLE Tasks(
            TaskID integer,
            Description text,
            Deadline date,
            Created timestamp,
            Completed timestamp,
            ProjectID integer,
            UserID decimal(21),
            PRIMARY KEY(TaskID),
            FOREIGN KEY(ProjectID) REFERENCES Projects(ProjectID),
            FOREIGN KEY(UserID) REFERENCES Users(UserID));""")
        
        #create project table
        cursor.execute("""CREATE TABLE Projects(
            ProjectID integer,
            Description text,
            Deadline date,
            Created timestamp,
            Completed timestamp,
            UserID decimal(21),
            PRIMARY KEY(ProjectID),
            FOREIGN KEY(UserID) REFERENCES Users(UserID));""")

        # create user table
        cursor.execute("""CREATE TABLE Users(
                            UserID decimal(21),
                            Username text,
                            Password date,
                            Created timestamp,
                            PRIMARY KEY(UserID));""")

        db.commit()


def create_user(username, password):
    with sqlite3.connect("to_do.db") as db:
        cursor = db.cursor()
        cursor.execute("PRAGMA Foreign_Keys = ON")
        userID = 1
        sql_query = "INSERT INTO Users(UserID, Username, Password, Created) VALUES (?,?,?,?)"
        cursor.execute(sql_query, (userID, username, password, datetime.now()))
        db.commit()


