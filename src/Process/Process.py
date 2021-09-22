import spacy
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
from tqdm import tqdm
from rank_bm25 import BM25Okapi
import time
from collections import defaultdict
from heapq import nlargest
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from operator import itemgetter
from .ProcessFiles import ProcessFiles
from src.Entity.ChatResponse import ChatResponse
from src.Entity.Files import Files
from .Thread import Thread
from .Resume import Resume
from .Tools import Tools

class Process:
  
    def initProcess(database, process):
        action = process['action']
        print(action)
        text = process['request_query']
        file = process['file']
        hash = Tools.encodeBase64(text)

        file = Files.getFiles(database, file)

        process['type'] = file[0]['type']

        process['hash'] = hash
        
        chat_response = ChatResponse.getChatResponse(database, hash)

        if len(chat_response) > 0:
            return chat_response[0]['response']
        else:
            if action == "query":
                db = database
                Thread(db, process).start()
                response = {"status": "process", "message": "Ainda não sei a resposta, estou aprendendo..."}
                return response
            elif action == "resume":
                resume = Resume.resumeFile(process)
                # if text:
                #     resume = json.dumps(resume, indent = 4) 
                #     insert = database.execute('INSERT INTO explain.chat_response (hash, text, response) VALUES (%s,%s, %s)', (hash, text, resume))
                #     if(insert):
                #         return resume
                #     else:
                #         return "Erro ao inserir texto"
                return resume
            else:
                return "Erro ao resumir texto"
        

