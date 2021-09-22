
class Files:
    def getFiles(database, name_file):
        database.execute("SELECT * FROM explain.files_jarvis WHERE name=%s", (name_file,))
        data = database.fetchall()
        return data
        
