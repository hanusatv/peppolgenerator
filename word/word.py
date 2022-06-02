import zipfile
import pandas
import shutil
import docx2pdf
import os
import base64
import tempfile


def wordTemplateToBase64(localization):
    with tempfile.TemporaryDirectory(prefix="peppolgenerator-") as tmpdir:
        df = pandas.read_excel('variables.xlsx', index_col=0, usecols=['KEY', localization],
                               keep_default_na=False)
        dictdata = df.to_dict()
        with zipfile.ZipFile('word.docx', 'r') as zip_ref:
            zip_ref.extractall(os.path.join(tmpdir, 'zipped'))
        with open(os.path.join(tmpdir, 'zipped/word/document.xml'), 'r', encoding='utf8') as f:
            data = f.read()
        document = data
        for key_translation, value_translation in dictdata[localization].items():
            document = document.replace(
                f'#{key_translation}#', str(value_translation))
        # Generer oversatte filer
            with open(os.path.join(tmpdir, 'zipped/word/document.xml'), 'w', encoding='utf-8-sig') as f:
                f.write(document)
        shutil.make_archive(os.path.join(tmpdir, 'denmark'),
                            'zip', os.path.join(tmpdir, 'zipped'))
        os.rename(os.path.join(tmpdir, 'denmark.zip'),
                  os.path.join(tmpdir, 'denmark.docx'))
        docx2pdf.convert(os.path.join(tmpdir, 'denmark.docx'),
                         os.path.join(tmpdir, 'denmark.pdf'))
        with open(os.path.join(tmpdir, 'denmark.pdf'), "rb") as pdf_file:
            encoded_string = base64.b64encode(pdf_file.read())
        pure_string = encoded_string.decode('utf-8')
    return pure_string


wordTemplateToBase64('DK')
