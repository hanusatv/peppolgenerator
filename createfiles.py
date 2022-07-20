import os
import yaml
import datetime
import base64
import pandas
import shutil
import tempfile
import zipfile
import docx2pdf
import pythoncom


def loadsettings(subdir):
    with open(os.path.join(subdir, 'settings.yaml'), 'r', encoding='utf-8') as f:
        subdirSettings = yaml.safe_load(f)
    return subdirSettings


def readXmlTemplate(path):
    with open(path, 'r', encoding='utf8') as f:
        data = f.read()
        return data


def createfiles(subdir):

    # Load all settings in the subdirectory
    settings = loadsettings(subdir)
    XML_TEMPLATE_FILE = settings['XML_TEMPLATE_FILE']
    XML_VARIABLES_FILE = settings['XML_VARIABLES_FILE']
    WORD_TEMPLATE_FILE = settings['WORD_TEMPLATE_FILE']
    WORD_VARIABLES_FILE = settings['WORD_VARIABLES_FILE']
    INCLUDED_LOCALIZATONS = settings['INCLUDED_LOCALIZATONS']

    # Check if .docx should be embedded
    attachmentBool = True if settings['WORD_TEMPLATE_FILE'] else False

    # Read .xml variables
    xml_df = pandas.read_excel(os.path.join(
        subdir, XML_VARIABLES_FILE), index_col=0, keep_default_na=False, usecols=['KEY']+INCLUDED_LOCALIZATONS)
    xml_dictdata = xml_df.to_dict()

    # Read .xml template and create placeholder for localized .xml files
    xmlTemplatePath = os.path.join(subdir, XML_TEMPLATE_FILE)
    template = readXmlTemplate(xmlTemplatePath)
    documents = {}

    # Create output directory
    outputdirname = datetime.datetime.now().strftime('%d-%m-%Y %H %M %S')
    os.mkdir(os.path.join(subdir, outputdirname))

    for country, dict_country in xml_dictdata.items():
        documents[country] = template
        for key_translation, value_translation in dict_country.items():
            documents[country] = documents[country].replace(
                f'<!-- {key_translation}-->', str(value_translation))
        if attachmentBool:
            word_df = pandas.read_excel(os.path.join(
                subdir, WORD_VARIABLES_FILE), index_col=0, keep_default_na=False, usecols=['KEY']+[country])
            word_dictdata = word_df.to_dict()

            # Create temp director to extract all .docx files to
            with tempfile.TemporaryDirectory(prefix="peppolgenerator-") as tmpdir:
                with zipfile.ZipFile(os.path.join(subdir, WORD_TEMPLATE_FILE), 'r') as zip_ref:
                    zip_ref.extractall(os.path.join(tmpdir, 'unzipped'))
                with open(os.path.join(tmpdir, 'unzipped/word/document.xml'), 'r', encoding='utf8') as f:
                    data = f.read()
                document = data
                for key_translation, value_translation in word_dictdata[country].items():
                    document = document.replace(
                        f'#{key_translation}#', str(value_translation))
                with open(os.path.join(tmpdir, 'unzipped/word/document.xml'), 'w', encoding='utf-8-sig') as f:
                    f.write(document)
                shutil.make_archive(os.path.join(tmpdir, 'zipped'),
                                    'zip', os.path.join(tmpdir, 'unzipped'))
                os.rename(os.path.join(tmpdir, 'zipped.zip'),
                          os.path.join(tmpdir, 'zipped.docx'))
                pythoncom.CoInitialize()
                docx2pdf.convert(os.path.join(tmpdir, 'zipped.docx'),
                                 os.path.join(tmpdir, 'base64encoded.pdf'), 'keep-active')
                shutil.copyfile(os.path.join(tmpdir, 'base64encoded.pdf'), os.path.join(
                    subdir, outputdirname, f'{country}.pdf'))
                with open(os.path.join(tmpdir, 'base64encoded.pdf'), "rb") as pdf_file:
                    encoded_string = base64.b64encode(pdf_file.read())
                pure_string = encoded_string.decode('utf-8')

            documents[country] = documents[country].replace(
                '<!-- ATTACHMENT-->', pure_string)
        filename = f'{country} - {XML_TEMPLATE_FILE}'
        with open(os.path.join(subdir, outputdirname, filename), 'w', encoding='utf-8-sig') as f:
            f.write(documents[country])
    return('Completed')
