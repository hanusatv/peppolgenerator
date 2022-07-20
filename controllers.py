from operator import inv
import os
import json
import pandas
import yaml


df = pandas.read_excel('C:/Users/hadis/source/repos/peppolgenerator/files/inv 1/variables.xlsx', index_col=0,
                       keep_default_na=False)
dfHead = list(df.columns)
# print(dfHead)


def getdir():
    FILES_DIR = getroot()

    invoiceFolder = {}

    for root, dirs, files in os.walk(FILES_DIR):
        if root == FILES_DIR:
            for invDir in dirs:
                key = os.path.join(root, invDir)
                invoiceFolder[key] = {}
        elif root in invoiceFolder:
            invoiceFolder[root]['files'] = files
            invoiceFolder[root]['dirs'] = dirs
            # Check if settings exist
            if 'settings.yaml' in invoiceFolder[root]['files']:
                with open(os.path.join(root, 'settings.yaml'), 'r', encoding='utf-8') as file:
                    settings = yaml.safe_load(file)
                    invoiceFolder[root]['settings'] = settings
                    if settings['XML_VARIABLES_FILE'] != None:
                        df = pandas.read_excel(os.path.join(root, settings['XML_VARIABLES_FILE']), index_col=0,
                                               keep_default_na=False)
                        invoiceFolder[root]['localizations'] = list(df.columns)
                    else:
                        invoiceFolder[root]['localizations'] = []
            else:
                invoiceFolder[root]['settings'] = {}
    return invoiceFolder


def setroot(path):
    with open('data.json', 'r', encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)

    data['rootdir'] = path

    with open('data.json', 'w', encoding='utf-8') as jsonFile:
        json.dump(data, jsonFile)


def getroot():
    with open('data.json', 'r', encoding='utf-8') as jsonFile:
        data = json.load(jsonFile)
        if data != None:
            return(data['rootdir'])


def setsettings(subdir, xmlTemplate, xmlVariables, wordTemplate, wordVariables, localizations):
    settings = {
        'XML_TEMPLATE_FILE': xmlTemplate,
        'XML_VARIABLES_FILE': xmlVariables,
        'WORD_TEMPLATE_FILE': wordTemplate,
        'WORD_VARIABLES_FILE': wordVariables,
        'INCLUDED_LOCALIZATONS': localizations
    }

    with open(os.path.join(subdir, 'settings.yaml'), 'w', encoding='utf-8') as yamlfile:
        yaml.dump(settings, yamlfile)
        return


##
# Test
##


def loadsettings(subdir):
    with open(os.path.join(subdir, 'settings.yaml'), 'r', encoding='utf-8') as f:
        subdirSettings = yaml.safe_load(f)
    print(subdirSettings)
