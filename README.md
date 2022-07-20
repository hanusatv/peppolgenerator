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
Run the `runservice.ps1` script with powershell. The application will start on http://localhost:9400.

To set the root directory, paste the path into the root directory field, and select __Save root directory__.
Next, you need to map the template files, and variables files by selecting them from the dropdown menues, and select __Save settings__.
The localizations from the XML variables will be listed, and then you need activate the localizations you want to generate copies of, and select __Save settings__ once again.
To generate localized copies of the templates, simply select __Create files__.


![image](https://user-images.githubusercontent.com/46691180/180037019-39adacfa-a466-455e-af71-5716c049e83f.png)



## Additional info
When inserting tags into the .docx file, you have to enter the whole tag in one go, and then save the file.
If you edit a pre-existing tag, then Word will save the tag as two separate strings, eventough it looks as if it's only one single string.
You therefore need to delete the whole paragraph, save the file, and then type in the whole tag again and save.
Word will then save the tag as one single string, and not two.
