from flask_mysqldb import MySQL
import MySQLdb.cursors
import json

class Users:
    def getUser(database,user_id):
        database.execute("SELECT * FROM `heroku_8a1f058f1608fe5`.`users` AS user  WHERE user.user_id = %s", (user_id, ))
        data = database.fetchall()
        return data

    def insertUser(database,  user_id, first_name):
        insert = database.execute("INSERT INTO `heroku_8a1f058f1608fe5`.`users`  (user_id, first_name) VALUES (%s, %s)", (user_id, first_name,))
        print("Insert")
        print(insert)
        if(insert):
            print("Sucesso ao inserir")
            return insert;
        else:
            return False;