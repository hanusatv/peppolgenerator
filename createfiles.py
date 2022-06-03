import os
import yaml
import datetime
import base64
import pandas
import shutil
import tempfile
import zipfile
import docx2pdf


def loadsettings():
    with open('settings.yaml', 'r', encoding='utf-8') as f:
        settings = yaml.safe_load(f)
        return settings

settings = loadsettings()

FILES_DIR = 'files'
ACTIVE_DIR = os.path.join(FILES_DIR, settings['ACTIVE_DIR'])
XML_TEMPLATE_FILE_NAME = settings['XML_TEMPLATE_FILE']
XML_TEMPLATE_FILE = os.path.join(ACTIVE_DIR, settings['XML_TEMPLATE_FILE'])
if settings['WORD_TEMPLATE_FILE'] != '':
    WORD_TEMPLATE_FILE = os.path.join(ACTIVE_DIR, settings['WORD_TEMPLATE_FILE'])
XML_VARIABLES_FILE = os.path.join(ACTIVE_DIR, settings['XML_VARIABLES_FILE'])
if settings['WORD_VARIABLES_FILE'] != '':
    WORD_VARIABLES_FILE = os.path.join(ACTIVE_DIR, settings['WORD_VARIABLES_FILE'])

if settings['WORD_TEMPLATE_FILE'] != '':
    df = pandas.read_excel(WORD_VARIABLES_FILE, index_col=0,
                            keep_default_na=False)


def readXmlTemplate():
    with open(XML_TEMPLATE_FILE, 'r', encoding='utf8') as f:
        data = f.read()
        return data

# Make const that is word variables that can be used for each loop by filtering


def createfiles():
    df = pandas.read_excel(
        XML_VARIABLES_FILE, index_col=0, keep_default_na=False)
    dictdata = df.to_dict()
    documents = {}
    template = readXmlTemplate()
    outputdirname = datetime.datetime.now().strftime('%m-%d-%Y %H %M %S')
    os.mkdir(os.path.join(ACTIVE_DIR, outputdirname))
    for country, dict_country in dictdata.items():
        documents[country] = template
        for key_translation, value_translation in dict_country.items():
            documents[country] = documents[country].replace(
                f'<!-- {key_translation}-->', str(value_translation))
        if WORD_TEMPLATE_FILE != "":
            base64pdf = wordTemplateToBase64(country)
            documents[country] = documents[country].replace(
                '<!-- ATTACHMENT-->', base64pdf)
    # Generer oversatte filer
        filename = f'{country} - {XML_TEMPLATE_FILE_NAME}'
        with open(os.path.join(ACTIVE_DIR, outputdirname, filename), 'w', encoding='utf-8-sig') as f:
            f.write(documents[country])


def wordTemplateToBase64(localization):
    with tempfile.TemporaryDirectory(prefix="peppolgenerator-") as tmpdir:
        dictdata = df[[localization]].to_dict()
        with zipfile.ZipFile(WORD_TEMPLATE_FILE, 'r') as zip_ref:
            zip_ref.extractall(os.path.join(tmpdir, 'unzipped'))
        with open(os.path.join(tmpdir, 'unzipped/word/document.xml'), 'r', encoding='utf8') as f:
            data = f.read()
        document = data
        for key_translation, value_translation in dictdata[localization].items():
            document = document.replace(
                f'#{key_translation}#', str(value_translation))
        # Generer oversatte filer
            with open(os.path.join(tmpdir, 'unzipped/word/document.xml'), 'w', encoding='utf-8-sig') as f:
                f.write(document)
        shutil.make_archive(os.path.join(tmpdir, 'zipped'),
                            'zip', os.path.join(tmpdir, 'unzipped'))
        os.rename(os.path.join(tmpdir, 'zipped.zip'),
                  os.path.join(tmpdir, 'zipped.docx'))
        docx2pdf.convert(os.path.join(tmpdir, 'zipped.docx'),
                         os.path.join(tmpdir, 'base64encoded.pdf'))
        with open(os.path.join(tmpdir, 'base64encoded.pdf'), "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        pure_string = encoded_string.decode('utf-8')
    return pure_string


createfiles()
