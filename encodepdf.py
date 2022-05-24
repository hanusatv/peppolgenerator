import base64

with open("test.pdf", "rb") as pdf_file:
    encoded_string = base64.b64encode(pdf_file.read())
    pure_string = encoded_string.decode('utf-8')
    print(pure_string)
