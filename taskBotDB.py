import mysql.connector

class BotDB:

    def __init__(self):
        self.connection = mysql.connector.connect(
            user='root',
            host='127.0.0.1',
            password='root_15YK',
            database='taskmanagementdb'
        )
        self.cursor = self.connection.cursor()

    def show_all_users(self):
        self.cursor.execute('SELECT * FROM users')
        users = self.cursor.fetchall()
        for row in users:
            print(row)