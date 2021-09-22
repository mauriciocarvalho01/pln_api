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
# from src.Entity.ChatResponse import ChatResponse
import base64
import json 
from src.Entity.Files import Files

class Process:
  
    def initProcess(database, process):
        action = process['action']
        print(action)
        text = process['request_query']
        file = process['file']
        hash = Process.encodeBase64(text)

        file = Files.getFiles(database, file)

        process['type'] = file[0]['type']
        
        database.execute("SELECT * FROM explain.chat_response WHERE hash=%s", (hash,))
        data = database.fetchall()

        if len(data) > 0:
            return data[0]['response']
        else:
            if action == "query":
                response =  Process.querySentence(process)
                response = json.dumps(response, indent = 4) 
                insert = database.execute('INSERT INTO explain.chat_response (hash, text, response) VALUES (%s,%s, %s)', (hash, text, response))
                print("Insert")
                print(insert)
                if(insert):
                    return response
                else:
                    return "Erro ao inserir a query"
            elif action == "resume":
                resume = Process.resumeFile(process)
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
        
    def querySentence(process):

        request_query = process['request_query']
        file = process['file']
        type_file = process['type']
        number_of_pages = 0
        text = ""
        if type_file == "pdf":
            number_of_pages = ProcessFiles.getNumberOfPdfPages(file)
        elif type_file == "docx":
            text = ProcessFiles.readDocx(file)
            number_of_pages = 1

        res = []
        total_sentencas = 0
            
        t0 = time.time()
        page = 0
        while(page < number_of_pages):

            if type_file == "pdf":
                text = ProcessFiles.readPdf(file, page)

            nlp = spacy.load("pt_core_news_sm")

            tok_text=[] # for our tokenised corpus
            sentencas = sent_tokenize(text)
            stopword = set(stopwords.words('portuguese') + list(punctuation))

            palavras_sem_stopwords = [palavra for palavra in sentencas if palavra not in stopword]
            
            text_lower = []
            for item in palavras_sem_stopwords:
                text_lower.append(item.lower())

            total_sentencas += len(sentencas)

            for doc in tqdm(nlp.pipe(text_lower, disable=["tagger", "parser","ner"])):
                tok = [t.text for t in doc if t.is_alpha]
                tok_text.append(tok)

            bm25 = BM25Okapi(tok_text)

            query = request_query
            tokenized_query = query.lower().split(" ")

        
            doc_scores = bm25.get_scores(tokenized_query)

            results = bm25.get_top_n(tokenized_query, palavras_sem_stopwords, n=3)
            
            text_filter = ""
            for sentencas in results:
                text_filter += sentencas
                repository = (sum(doc_scores), text_filter)
                res.append(repository)
            # print(repository)
                
            print(f'Pagina {page} \n')
            
            page = page + 1                             

        t1 = time.time()
        print(f'Foi analisado {total_sentencas} sentenças em {round(t1-t0,3) } segundos \n')
        res =  sorted(res,key=itemgetter(0), reverse=True)
        response = {
            "time": str(t1-t0) + " segundos",
            "response": res[0:4]
        }

        return response

    def resumeFile(process):

        request_query = process['request_query']
        file = process['file']
        type_file = process['type']

        number_of_pages = 0
        text = ""
        if type_file == "pdf":
            number_of_pages = ProcessFiles.getNumberOfPdfPages(file)
        elif type_file == "docx":
            text = ProcessFiles.readDocx(file)
            number_of_pages = 1

        res = []
        total_sentencas = 0
        res = ""
        
        t0 = time.time()
        page = 0
        while(page < number_of_pages):
            if type_file == "pdf":
                text = ProcessFiles.readPdf(file, page)

            sentencas = sent_tokenize(text)
            palavras = word_tokenize(text.lower())

            total_sentencas += len(sentencas)

            stopword = set(stopwords.words('portuguese') + list(punctuation))
            palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopword]
            
            frequencia = FreqDist(palavras_sem_stopwords)
            sentencas_importantes = defaultdict(int)

            for i, sentenca in enumerate(sentencas):
                for palavra in word_tokenize(sentenca.lower()):
                    if palavra in frequencia:
                        sentencas_importantes[i] += frequencia[palavra]

            idx_sentencas_importantes = nlargest(3, sentencas_importantes, sentencas_importantes.get)

            for i in sorted(idx_sentencas_importantes):
                res += sentencas[i]

            print(f'Pagina {page} \n')
            
            page = page + 1 

        t1 = time.time()
        print(f'Foi analisado {total_sentencas} sentenças em {round(t1-t0,3) } segundos \n')

        response = {
            "time": str(t1-t0) + " segundos",
            "response": res
        }

        return response

    def encodeBase64(text):
        text = text.encode("ascii", 'ignore')
        hash = base64.b64encode(text)
        hash = hash.decode("ascii")
        return hash