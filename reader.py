from services import QnA
from services import Luis
from  credential import Credential



FILE_NAME = 'credentials.txt'

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.rstrip() for line in file]
    except IOError:
        print(f'Error: File { file_name } file does not exist !!!')

def match(attrib, other):
    attrib = attrib.lower().strip()
    return True if attrib == other else False

def read_credentials():
    lines = read_file(FILE_NAME)
    credential = None
    new_credentials = []

    for line in lines:
        if not not ''.join(line.split()):
            data = line.split(':')

            if len(data) >= 2:
                attrib = data[0].strip()
                value  = data[1].strip()

                if match(attrib, 'type'):
                    if credential is not None and credential.complete():
                        new_credentials.append(credential)
                        credential = None

                    credential = Credential(value, None, None, None, 
                                            None, None, None)
                if credential is not None:
                    if match(attrib, 'name'):
                        credential.app_name = value
                    if match(attrib, 'version'):
                        credential.app_version = value
                    if match(attrib, 'key'):
                        credential.app_key = value
                    if match(attrib, 'region'):
                        credential.app_region = value
                    if match(attrib, 'host'):
                        frag = data[2].strip()
                        value = value + frag
                        credential.app_host = value
                    if match(attrib, 'id'):
                        credential.app_id = value

    if credential is not None and credential.complete():
        new_credentials.append(credential)

    return new_credentials

def read_for_qna():
    pass

def read_for_luis():
    pass