import sqlite3

connection = sqlite3.connect('web_project_database.db3')
cursor = connection.cursor()

cursor.execute(
    '''CREATE TABLE IF NOT EXISTS student (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, name VARCHAR (32))'''
               )
connection.commit()
cursor.close()
connection.close()
