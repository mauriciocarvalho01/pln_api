from flask_mysqldb import MySQL
import MySQLdb.cursors
import json

class Files:
    def getFiles(database, id_file, user_id):
        database.execute("SELECT * FROM `explain`.`files_jarvis` AS files INNER JOIN `explain`.`users` AS user USING(user_id) WHERE files.id = %s AND user.user_id = %s", (id_file,user_id))
        data = database.fetchall()
        return data

    def createFileResponse(response,process):
        hash = process['hash']
        with open(f'storage/{hash}.json', 'w') as f:
            json.dump(response, f, indent=2)
        print("New json file is created from"  + process['hash'] + ".json file")
        return True
        
    def allFiles(database, user_id):
        database.execute("SELECT * FROM `explain`.`files_jarvis` AS files INNER JOIN `explain`.`users` AS user USING(user_id) WHERE user.user_id = %s", (user_id,))
        data = database.fetchall()
        return data