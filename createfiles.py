import os
import yaml
import datetime
import base64
import pandas
import shutil
import tempfile
import zipfile
import docx2pdf

FILES_DIR = 'files'


def loadsettings():
    settings = {}
    with open('settings.yaml', 'r', encoding='utf-8') as f:
        activeDir = yaml.safe_load(f)
        settings['activedir'] = activeDir
    with open(os.path.join(FILES_DIR, settings['activedir']['ACTIVE_DIR'], 'settings.yaml'), 'r', encoding='utf-8') as f:
        activeDirSettings = yaml.safe_load(f)
        settings['activeDirSettings'] = activeDirSettings
    return settings


settings = loadsettings()

ACTIVE_DIR = os.path.join(FILES_DIR, settings['activedir']['ACTIVE_DIR'])
XML_TEMPLATE_FILE_NAME = settings['activeDirSettings']['XML_TEMPLATE_FILE']
XML_TEMPLATE_FILE = os.path.join(
    ACTIVE_DIR, settings['activeDirSettings']['XML_TEMPLATE_FILE'])
XML_VARIABLES_FILE = os.path.join(
    ACTIVE_DIR, settings['activeDirSettings']['XML_VARIABLES_FILE'])
if settings['activeDirSettings']['WORD_TEMPLATE_FILE'] != None:
    WORD_TEMPLATE_FILE = os.path.join(
        ACTIVE_DIR, settings['activeDirSettings']['WORD_TEMPLATE_FILE'])
    WORD_VARIABLES_FILE = os.path.join(
        ACTIVE_DIR, settings['activeDirSettings']['WORD_VARIABLES_FILE'])
    attachmentBool = True
else:
    attachmentBool = False

if settings['activeDirSettings']['WORD_TEMPLATE_FILE'] != None:
    df = pandas.read_excel(WORD_VARIABLES_FILE, index_col=0,
                           keep_default_na=False)


def readXmlTemplate():
    with open(XML_TEMPLATE_FILE, 'r', encoding='utf8') as f:
        data = f.read()
        return data


def createfiles():
    df = pandas.read_excel(
        XML_VARIABLES_FILE, index_col=0, keep_default_na=False)
    dictdata = df.to_dict()
    documents = {}
    template = readXmlTemplate()
    outputdirname = datetime.datetime.now().strftime('%d-%m-%Y %H %M %S')
    os.mkdir(os.path.join(ACTIVE_DIR, outputdirname))
    for country, dict_country in dictdata.items():
        documents[country] = template
        for key_translation, value_translation in dict_country.items():
            documents[country] = documents[country].replace(
                f'<!-- {key_translation}-->', str(value_translation))
        if attachmentBool:
            base64pdf = wordTemplateToBase64(country, outputdirname)
            documents[country] = documents[country].replace(
                '<!-- ATTACHMENT-->', base64pdf)
        filename = f'{country} - {XML_TEMPLATE_FILE_NAME}'
        with open(os.path.join(ACTIVE_DIR, outputdirname, filename), 'w', encoding='utf-8-sig') as f:
            f.write(documents[country])


def wordTemplateToBase64(localization, outputdirname):
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
        shutil.copyfile(os.path.join(tmpdir, 'base64encoded.pdf'), os.path.join(
            ACTIVE_DIR, outputdirname, f'{localization}.pdf'))
        with open(os.path.join(tmpdir, 'base64encoded.pdf'), "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        pure_string = encoded_string.decode('utf-8')
    return pure_string


createfiles()
