import base64

def getbase64string(path):
    with open(path, "rb") as pdf_file:
        encoded_string = base64.b64encode(pdf_file.read())
        pure_string = encoded_string.decode('utf-8')
        return(pure_string)
