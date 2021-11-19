from flask_mysqldb import MySQL
import MySQLdb.cursors
from src.Process.Tools import Tools
import json
import os

class ChatResponse:
    def getChatResponse(database, hash):
        database.execute("SELECT response FROM heroku_54c63117db00862.chat_response WHERE hash=%s", (hash,))
        data = database.fetchall()
        return data

    def insertChatResponse(database, response, process):
        response = json.dumps(response, indent = 4) 
        text = process['request_query']
        hash = Tools.encodeBase64(text)
        check_exists = ChatResponse.getChatResponse(database, hash)
        inserted = []
        if len(check_exists) == 0: 
            insert = database.execute('INSERT INTO heroku_54c63117db00862.chat_response (hash, text, response) VALUES (%s,%s, %s)', (hash, text, response))
            print("Insert")
            print(insert)
            if(insert):
                inserted.append(response)
                print("Sucesso ao inserir")
                os.remove(f"storage/{hash}.json")
                return inserted; 
            else:
                print("Erro ao inserir")
                return []
        else: 
            inserted = []
            inserted.append(response)
            return inserted; 


    def updateChatResponse(database, process):
        try:
            hash = process['hash']
            with open(f'storage/{hash}.json') as f:
                data = json.load(f)
            return ChatResponse.insertChatResponse(database, data, process)
        except IOError:
            response = []
            data = ChatResponse.getChatResponse(database, hash)
            if(len(data) > 0):
                response.append(data[0]['response'])
            return response
    


