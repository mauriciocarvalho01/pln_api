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
        user_id = process['user_id']
        print(user_id)
        hash = Tools.encodeBase64(text)

        file = Files.getFiles(database, file, user_id)
        print(file)

        if len(file) == 0:
            return {"status": "erro", "message": "Não achei nenhum arquivo cadastrado"}
        process['type'] = file[0]['type']

        process['hash'] = hash

        chat_response = []
        if action == 'query':
            chat_response = ChatResponse.updateChatResponse(database, process)


        if len(chat_response) > 0:
            # print("chat_response")
            # print(chat_response)
            response = chat_response[0]
            return response
        else:
            if action == "query":
                db = database
                Thread(db, process).start()
                response = {"status": "learning", "message": "Ainda não sei a resposta, estou aprendendo...Pergunte - me novamente em instantes"}
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
        

