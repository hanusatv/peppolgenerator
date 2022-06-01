import os, zipfile
os.system('copy word.docx word.zip')

with zipfile.ZipFile("word.zip","r") as zip_ref:
    zip_ref.extractall("zipped")

with open('zipped/word/document.xml') as xmldoc:
    data = xmldoc.read()
    print(data)