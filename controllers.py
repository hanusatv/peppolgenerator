import os
ROOT_DIR = os.path.dirname(os.path.realpath(__file__))
FILES_DIR = os.path.join(ROOT_DIR, 'files')
for root, directories, files in os.walk(FILES_DIR, topdown=True):
    for name in files:
        print(os.path.join(root, name))
    for name in directories:
        print(os.path.join(root, name))
