# import the threading module
import threading
import json 
from .Search import Search
from .Tools import Tools
from flask_mysqldb import MySQL
import MySQLdb.cursors
from src.Entity.Files import Files

class Thread(threading.Thread):
    def __init__(self, database, process):
        threading.Thread.__init__(self)
        self.process = process
        self.database = database
 
        # helper function to execute the threads
    def run(self):
        response = Search.querySentence(self.process) 
        Files.createFileResponse(response, self.process)  

        