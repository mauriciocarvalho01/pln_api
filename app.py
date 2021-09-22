# Faz os imports utilizados

from flask import Flask, request, jsonify, render_template
import base64
from src.Process.Process import Process
from src.Process.ProcessFiles import ProcessFiles
from flask_mysqldb import MySQL
import MySQLdb.cursors


app = Flask(__name__)     # Iniciando a aplicação.
app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'explain'
mysql = MySQL(app)



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

@app.route('/pln', methods=['POST'])
def home():
    request_query = request.json.get("query")
    file = request.json.get("file")
    action = request.json.get("action")
    database = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    process = { "request_query": request_query, "file": file, "action": action }   
    result = Process.initProcess(database, process)
    database.close()
    return result

# Executa a aplição na porta 3000 (localhost)
if __name__ == "__main__":
    app.run(debug=True)



