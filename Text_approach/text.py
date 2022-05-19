with open('template.xml', 'r', encoding='utf8') as f:
    data = f.read()
    f.close()

print(type(data))
#replaced = data.replace("{DOKUMENTID}", "Panus")


#with open("test2.xml", "w") as f:
#    f.write(replaced)