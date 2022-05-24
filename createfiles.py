import csv, os, yaml, datetime

def loadsettings():
    with open("settings.yaml","r",encoding="utf-8") as f:
        settings = yaml.safe_load(f)
        return settings
settings = loadsettings()

FILES_DIR = "files"
ACTIVE_DIR = settings["ACTIVE_DIR"]
TEMPLATE_FILE = settings["TEMPLATE_FILE"]
VARIABLES_FILE = settings["VARIABLES_FILE"]
CSV_DELIMITER = settings["CSV_DELIMITER"]

def readtemplate():
    with open(os.path.join(FILES_DIR,ACTIVE_DIR,TEMPLATE_FILE), 'r', encoding='utf8') as f:
        data = f.read()
        return data

def createfiles():
    countrylist = []
    with open(os.path.join(FILES_DIR,ACTIVE_DIR,VARIABLES_FILE), newline="", encoding="utf-8-sig") as f:
        csv_reader = csv.DictReader(f, delimiter=CSV_DELIMITER)
        countrylist = csv_reader.fieldnames[1:]
        documents = {}
        template = readtemplate()
        for country in countrylist:
            documents[country] = template
        for row in csv_reader:
            for country in countrylist:
                documents[country] = documents[country].replace(
                    f'<!-- {row["KEY"]}-->', row[country])
        #Generer oversatte filer
        outputdirname = TEMPLATE_FILE + " " + datetime.datetime.now().strftime("%m-%d-%Y %H %M %S")
        os.mkdir(os.path.join(FILES_DIR,ACTIVE_DIR,outputdirname))
        for country in countrylist:
            filename = f'{country} - {TEMPLATE_FILE}'
            with open(os.path.join(FILES_DIR,ACTIVE_DIR,outputdirname,filename), "w", encoding="utf-8-sig") as f:
                f.write(documents[country])

createfiles()
