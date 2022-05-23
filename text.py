import csv, os, yaml, datetime

def loadsettings():
    with open("settings.yaml","r",encoding="utf-8") as f:
        settings = yaml.safe_load(f)
        return settings
settings = loadsettings()

TEMPLATE_DIR = settings["TEMPLATE_DIR"]
VARIABLES_DIR = settings["VARIABLES_DIR"]
OUTPUT_DIR = settings["OUTPUT_DIR"]
TEMPLATE_FILE = settings["TEMPLATE_FILE"]
OUTPUT_FILE_NAME = settings["OUTPUT_FILE_NAME"]
VARIABLES_FILE = settings["VARIABLES_FILE"]
CSV_DELIMITER = settings["CSV_DELIMITER"]

def readtemplate():
    with open(os.path.join(TEMPLATE_DIR,TEMPLATE_FILE), 'r', encoding='utf8') as f:
        data = f.read()
        return data

def createfiles():
    countrylist = []
    with open(os.path.join(VARIABLES_DIR,VARIABLES_FILE), newline="", encoding="utf-8-sig") as f:
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
        formattednow = datetime.datetime.now().strftime("%m-%d-%Y %H %M %S")
        os.mkdir(os.path.join(OUTPUT_DIR,formattednow))
        for country in countrylist:
            filename = f'{country}-{OUTPUT_FILE_NAME}'
            with open(os.path.join(OUTPUT_DIR,formattednow,filename), "w", encoding="utf-8-sig") as f:
                f.write(documents[country])

createfiles()
