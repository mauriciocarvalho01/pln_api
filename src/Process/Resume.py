
import spacy
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from string import punctuation
import time
from collections import defaultdict
from heapq import nlargest
import nltk
nltk.download('punkt')
nltk.download('stopwords')
from .ProcessFiles import ProcessFiles


class Resume:
    def resumeFile(process):
        
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
            "type": process["action"],
            "status": "success",
            "response": res
        }

        return response