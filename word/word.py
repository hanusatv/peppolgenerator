import zipfile
import pandas
import shutil


def readtemplate():
    with zipfile.ZipFile("word.docx", "r") as zip_ref:
        zip_ref.extractall("zipped")
    with open('zipped/word/document.xml', 'r', encoding='utf8') as f:
        data = f.read()
        return data


def replacekeys():
    df = pandas.read_excel('variables.xlsx', index_col=0,
                           keep_default_na=False)
    dictdata = df.to_dict()
    documents = {}
    template = readtemplate()
    for country, dict_country in dictdata.items():
        documents[country] = template
        for key_translation, value_translation in dict_country.items():
            documents[country] = documents[country].replace(
                f'#{key_translation}#', str(value_translation))
    # Generer oversatte filer
        with open('zipped/word/document.xml', "w", encoding="utf-8-sig") as f:
            f.write(documents[country])
    shutil.make_archive('denmark', 'zip', 'zipped')
    shutil.copyfile('denmark.zip', 'denmark.docx')


readtemplate()
replacekeys()
