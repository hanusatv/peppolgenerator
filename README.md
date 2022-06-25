# peppolgenerator

Python script that generates multiple PEPPOL invoices with localized data.

## Installation

Install python from the [Microsoft Store](https://apps.microsoft.com/store/search/python), or directly from the [Python foundation](https://www.python.org/downloads/) if you're feeling advanced.

Install [Git for Windows](https://gitforwindows.org/).

Open your favourite terminal and clone this repository.
```
git clone https://github.com/hanusatv/peppolgenerator.git
```

CD into the peppolgenerator directory and install the required python modules.

```
pip install -r environmentRequirements.txt
```

## Usage
The repository is structured in sub-directories, where each sub-directory has its own set of templates and translations.
All sub-directories must be placed within the `...\peppolgenerator\files` directory.
The active directory is set in the `...\peppolgenerator\settings.yaml` file.
Each sub-directory must have a `settings.yaml` file containg mappings to the different files within itself.

### Example of sub-directory `settings.yaml`:
```
#XML template file you want to generate localized copies of.
XML_TEMPLATE_FILE: BC online - PEPPOL3 - Purchase Invoice 2 - Nod Publishers.xml
#Word template file you want to embed in the XML file. Must be a .docx file.
WORD_TEMPLATE_FILE: word.docx
#Variables file that contains translations of localized words for the .xml file. Must be a .xlsx file.
XML_VARIABLES_FILE: xmlvariables.xlsx
#Variables file that contains translations of localized words for the .docx file. Must be a .xlsx file.
WORD_VARIABLES_FILE: wordvariables.xlsx
```
The script will not try to embed a .pdf inside the .xml if `WORD_TEMPLATE_FILE:` attribute is left blank.

Once the settings for the active directory and sub-directory are set, CD into the root directory and run the script.
```
python createfiles.py
```

## Additional info
When inserting tags info the .docx file, you have to enter the whole tag in one go, and then save the file.
If you edit a pre-existing tag, then Word will save the tag as two separate strings, eventough it looks as if it's only one single string.
You therefore need to delete the whole paragraph, save the file, and then type in the whole tag again and save.
Word will then save the tag as one single string, and not two.
