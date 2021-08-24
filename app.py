# Faz os imports utilizados

from flask import Flask, request, jsonify, render_template
import PyPDF2
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



app = Flask(__name__)     # Iniciando a aplicação.
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def teste():
    params = "Deu certo porra"; 

    return jsonify(params)

@app.route('/pln', methods=['POST'])
def home():
    process = initProcess(request.json.get("query"))

    response = {
        "status": "processado",
        "tempo": process["time"],
        "resposta": process['response']
    }

    return response

def readPdf():
    pdf_file = open('modelo/colacao_grau.pdf', 'rb')
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    #pega o numero de páginas
    number_of_pages = read_pdf.getNumPages()
    

    #lê a primeira página completa
    page = read_pdf.getPage(2)

    #extrai apenas o texto
    page_content = page.extractText()

    
    # faz a junção das linhas
    # parsed = ''.join(page_content)

    # print("Sem eliminar as quebras")
    # print(parsed)

    # remove as quebras de linha
    # parsed = re.sub('\n', '', parsed)
    # print("Após eliminar as quebras")
    # print(parsed)
    return page_content.replace("\n", " ")

def initProcess(request_query):

    text = readPdf()
    nlp = spacy.load("pt_core_news_sm")

    tok_text=[] # for our tokenised corpus
    sentencas = sent_tokenize(text)

    text_lower = []
    for item in sentencas:
        text_lower.append(item.lower())


    #Tokenising using SpaCy:
    for doc in tqdm(nlp.pipe(text_lower, disable=["tagger", "parser","ner"])):
        tok = [t.text for t in doc if t.is_alpha]
        tok_text.append(tok)


    bm25 = BM25Okapi(tok_text)
    query = request_query
    tokenized_query = query.lower().split(" ")

    t0 = time.time()
    results = bm25.get_top_n(tokenized_query, sentencas, n=1)
    t1 = time.time()
    print(f'Foi analisado {len(sentencas)} sentenças em {round(t1-t0,3) } segundos \n')
    text_filter = ""
    for i in results:
      text_filter += i


    sentencas = sent_tokenize(text_filter)
    palavras = word_tokenize(text_filter.lower())

    stopword = set(stopwords.words('portuguese') + list(punctuation))
    palavras_sem_stopwords = [palavra for palavra in palavras if palavra not in stopword]
    
    frequencia = FreqDist(palavras_sem_stopwords)
    sentencas_importantes = defaultdict(int)

    for i, sentenca in enumerate(sentencas):
        for palavra in word_tokenize(sentenca.lower()):
            if palavra in frequencia:
                sentencas_importantes[i] += frequencia[palavra]

    idx_sentencas_importantes = nlargest(1, sentencas_importantes, sentencas_importantes.get)
    res = ""
    for i in sorted(idx_sentencas_importantes):
        res += sentencas[i]

    response = {
        "time": str(t1-t0) + " segundos",
        "response": res
    }

    return response

# Executa a aplição na porta 3000 (localhost)
if __name__ == "__main__":
    app.run(debug=True)



