# Faz os imports utilizados

from flask import Flask, request, jsonify, render_template
import os
from src.Process.Process import Process
from src.Process.ProcessFiles import ProcessFiles
from src.Entity.Files import Files
from flask_mysqldb import MySQL
import MySQLdb.cursors
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'storage/'
ALLOWED_EXTENSIONS = {'pdf','docx'}

app = Flask(__name__)     # Iniciando a aplicação.
app.config["DEBUG"] = True
app.config['MYSQL_HOST'] = 'us-cdbr-east-04.cleardb.com'
app.config['MYSQL_USER'] = 'b1a2a60a5c5674'
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_PASSWORD'] = 'b2e2c06a'
app.config['MYSQL_DB'] = 'heroku_8a1f058f1608fe5'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mysql = MySQL(app)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/', methods=['GET'])
def teste():
    return {"teste": "Opa"}

@app.route('/upload-file', methods=['GET','POST'])
def uploadFile():
    if request.method == 'POST':
        file = request.files['file']
        print(file.content_type);
        data = dict(request.form)
        email = data['email']; 
        print(email)
        database = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        name = file.filename.rsplit('.', 1)[0].lower();
        type = file.filename.rsplit('.', 1)[1].lower();
        insert = Files.saveFile(database, name, type, email)
        if(insert):   
            files = Files.allFiles(database, email)
            database.close()
            if file and allowed_file(file.filename):
                last_file = files[-1]
                filename = secure_filename(str(last_file['id']) + "." + file.filename.rsplit('.', 1)[1].lower());
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return {"erro": "arquivo não suportado"}
        else:
            return {"erro": "arquivo não suportado"}
    return {"message": "salvo"}


@app.route('/files/<user_id>', methods=['GET'])
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

@app.route('/files/<user_id>/<file_id>', methods=['GET']) 
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
    app.run(debug=True)



