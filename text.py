import csv
from re import template


def readtemplate():
    with open('template.xml', 'r', encoding='utf8') as f:
        data = f.read()
        return data


def readmapping():
    countrylist = []
    with open('variables.csv', newline="", encoding="utf-8-sig") as file:
        csv_reader = csv.DictReader(file, delimiter=";")
        countrylist = csv_reader.fieldnames[1:]
        documents = {}
        template = readtemplate()
        for country in countrylist:
            documents[country] = template
        for row in csv_reader:
            for country in countrylist:
                documents[country] = documents[country].replace(
                    f'<!-- {row["KEY"]}-->', row[country])
        for country in countrylist:
            with open(f'{country}-inv1.xml', "w", encoding="utf-8-sig") as file:
                file.write(documents[country])
        print(documents["ES"])
        # for row in csv_reader:
        #    for cell in countrylist:


readmapping()

#replaced = data.replace("{DOKUMENTID}", "Panus")


# with open("test2.xml", "w") as f:
#    f.write(replaced)
