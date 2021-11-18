# Faz os imports utilizados

from flask import Flask, request, jsonify, render_template
import base64
from src.Process.Process import Process
from src.Process.ProcessFiles import ProcessFiles
from src.Entity.Files import Files
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)     # Iniciando a aplicação.
app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'explain'
mysql = MySQL(app)

@app.route('/home', methods=['GET'])
def teste():
    return {"teste": "Opa"}

@app.route('/upload-file', methods=['POST'])
def uploadFile():
    file_base64 = request.json.get("file")
    filename = request.json.get("filename")
    type_file = request.json.get("type")
    database = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    saved = ProcessFiles.saveFile(database, file_base64, filename, type_file)
    database.close()

    if saved:
        return {"save": True}
    else:
        return {"save": False,"message": "Erro ao salvar arquivo"}

@app.route('/files/<user_id>', methods=['POST'])
def getAllFiles(user_id):
    # user_id = request.args.get('user_id')
    print(user_id)
    database = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    files = Files.allFiles(database, user_id)
    database.close()

    if len(files) == 0:
        return {"files": False}
    else:
        return {"files": files}

@app.route('/files/<user_id>/<file_id>', methods=['POST'])
def getFiles(user_id, file_id):
    # user_id = request.args.get('user_id')
    database = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    files = Files.getFiles(database, file_id, user_id)
    database.close()

    if len(files) == 0:
        return {"files": False}
    else:
        return {"files": files}

@app.route('/pln', methods=['POST'])
def home():
    print(request.json)
    request_query = request.json.get("query")
    file = request.json.get("file")
    action = request.json.get("action")
    user_id = request.json.get("user_id")
    database = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    process = { "request_query": request_query, "file": file, "action": action, "user_id": user_id}   
    result = Process.initProcess(database, process)

    return result

# Executa a aplição na porta 8000 (localhost)
if __name__ == "__main__":
    app.run(debug=True, host="192.168.1.187", port="8000")



