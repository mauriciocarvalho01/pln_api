
import PyPDF2
import os
from pathlib import Path
from base64 import b64decode
from docx import Document

class ProcessFiles:
    # def __init__(self, file: str):
    #     self.file = file
    def readPdf(file, page):
        pdf_file = open(f'storage/{file}.pdf', 'rb')
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        #pega o numero de páginas
        
        #lê a primeira página completa
        page = read_pdf.getPage(page)
        # remove as quebras de linha
        # parsed = re.sub('\n', '', parsed)
        # print("Após eliminar as quebras")
        # print(parsed)

        #extrai apenas o texto
        page_content = page.extractText()
        parsed = page_content.replace("\n", " ")
        
        # faz a junção das linhas
        parsed = ''.join(parsed)

        # print("Sem eliminar as quebras")
        # print(parsed)

        # remove as quebras de linha
        # parsed = re.sub('\n', '', parsed)
        # print("Após eliminar as quebras")
        # print(parsed)
        return parsed
        
    def getNumberOfPdfPages(file):
        try:
            # file_exists = os.path.exists(f'storage/{file}.pdf')
            pdf_file = open(f'storage/{file}.pdf', 'rb')
            read_pdf = PyPDF2.PdfFileReader(pdf_file)
            #pega o numero de páginas
            return read_pdf.getNumPages()
        except FileNotFoundError: 
            print("Não existe esse arquivo")
            return 0

    def getNumberOfDocxPages(file):
        # try:
        #     # file_exists = os.path.exists(f'storage/{file}.pdf')
        #     pdf_file = open(f'storage/{file}.docx', 'rb')
        #     read_pdf = PyPDF2.PdfFileReader(pdf_file)
        #     #pega o numero de páginas
        #     return read_pdf.getNumPages()
        # except FileNotFoundError: 
        #     print("Não existe esse arquivo")
            return 1

    def saveFile(database, file, filename, type_file):
        pdf_file = 'storage/'+filename+'.'+type_file

        insert = database.execute('INSERT INTO explain.files_jarvis (name, type) VALUES (%s,%s)', (filename, type_file))
        print("Insert")
        print(insert)
        if(insert):
            # Decode the Base64 string, making sure that it contains only valid characters
            bytes = b64decode(file, validate=True)

            if type_file == "pdf":
                # Perform a basic validation to make sure that the result is a valid PDF file
                # Be aware! The magic number (file signature) is not 100% reliable solution to validate PDF files
                # Moreover, if you get Base64 from an untrusted source, you must sanitize the PDF contents
                if bytes[0:4] != b'%PDF':
                    raise ValueError('Missing the PDF file signature')

            # Write the PDF contents to a local file
            f = open(pdf_file, 'wb')
            f.write(bytes)
            f.close()
            return True
        else:
            return "Erro ao inserir o arquivo"
        
    def readDocx(file):
        document = Document(f'storage/{file}.docx')
        text_repository = [p.text for p in document.paragraphs]
        
        text = ""
        for line in text_repository:
            text = text  + line
        return text