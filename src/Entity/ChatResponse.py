from flask_mysqldb import MySQL
import MySQLdb.cursors
from src.Process.Tools import Tools
import json

class ChatResponse:
    def getChatResponse(database, hash):
        database.execute("SELECT * FROM explain.chat_response WHERE hash=%s", (hash,))
        data = database.fetchall()
        return data

    def insertChatResponse(database, response, process):
        response = json.dumps(response, indent = 4) 
        text = process['request_query']
        hash = Tools.encodeBase64(text)
        insert = database.execute('INSERT INTO explain.chat_response (hash, text, response) VALUES (%s,%s, %s)', ("hash", "text", "response"))
        print("Insert")
        print(insert)
        if(insert):
            print("Sucesso ao inserir")
        else:
            print("Erro ao inserir")
    


