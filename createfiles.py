import os, yaml, datetime, base64, pandas

def loadsettings():
    with open("settings.yaml","r",encoding="utf-8") as f:
        settings = yaml.safe_load(f)
        return settings
settings = loadsettings()

FILES_DIR = "files"
ACTIVE_DIR = settings["ACTIVE_DIR"]
TEMPLATE_FILE = settings["TEMPLATE_FILE"]
VARIABLES_FILE = settings["VARIABLES_FILE"]

def getbase64string(path):
    with open(path, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
        pure_string = encoded_string.decode('utf-8')
        return(pure_string)

def readtemplate():
    with open(os.path.join(FILES_DIR,ACTIVE_DIR,TEMPLATE_FILE), 'r', encoding='utf8') as f:
        data = f.read()
        return data

def createfiles():
    df = pandas.read_excel(os.path.join(FILES_DIR,ACTIVE_DIR,VARIABLES_FILE),index_col=0,keep_default_na=False)
    dictdata = df.to_dict()
    documents = {}
    template = readtemplate()
    outputdirname = TEMPLATE_FILE + " " + datetime.datetime.now().strftime("%m-%d-%Y %H %M %S")
    os.mkdir(os.path.join(FILES_DIR, ACTIVE_DIR,outputdirname))
    for country, dict_country in dictdata.items():
        documents[country] = template
        for key_translation, value_translation in dict_country.items():
            documents[country] = documents[country].replace(
                f'<!-- {key_translation}-->', str(value_translation))
        pdffile = os.path.join(FILES_DIR,ACTIVE_DIR,f'{country}.pdf')
        if os.path.exists(pdffile):
            encodedpdf = getbase64string(pdffile)
            documents[country] = documents[country].replace("<!-- ATTACHMENT-->",encodedpdf)
    #Generer oversatte filer
        filename = f'{country} - {TEMPLATE_FILE}'
        with open(os.path.join(FILES_DIR,ACTIVE_DIR,outputdirname,filename), "w", encoding="utf-8-sig") as f:
            f.write(documents[country])

createfiles()
