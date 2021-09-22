from flask_mysqldb import MySQL
import MySQLdb.cursors
import json

class Files:
    def getFiles(database, name_file):
        database.execute("SELECT * FROM explain.files_jarvis WHERE name=%s", (name_file,))
        data = database.fetchall()
        return data

    def createFileResponse(response,process):
        hash = process['hash']
        with open(f'storage/{hash}.json', 'w') as f:
            json.dump(response, f, indent=2)
        print("New json file is created from"  + process['hash'] + ".json file")
        return True
        
    