from services import QnA
from services import Luis
from  credential import Credential




SPLIT_DATA = ':'
CREDENTIAL_NAME = 'credentials.txt'

def read_file(file_name):
    try:
        with open(file_name, 'r') as file:
            return [line.rstrip() for line in file]
    except IOError:
        print(f'Error: File { file_name } file does not exist !!!')

def match(attrib, other):
    attrib = attrib.lower().strip()
    return True if attrib == other else False

def find_credential(find, credentials):
    for credential in credentials:
        current = credential.app_name.lower()
        flag = find.lower().strip() == current

        if flag:
            return credential

    return f'Credential with name { find } does not exist !!!'

def read_credentials():
    lines = read_file(CREDENTIAL_NAME)
    credential = None
    new_credentials = []

    for line in lines:
        if not not ''.join(line.split()):
            data = line.split(SPLIT_DATA)

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
                        value = f'{ value }:{ frag }'
                        credential.app_host = value
                    if match(attrib, 'id'):
                        credential.app_id = value

    if credential is not None and credential.complete():
        new_credentials.append(credential)

    return new_credentials

def get_additional(value):
    try:
        return value.split('|')
    except:
        return value

def luis_for_qna(app_name, questions, dispatcher):
    dispatcher = find_credential(dispatcher, read_credentials())
    new_luis = []
    for question in questions:
        new_luis.append(Luis(dispatcher, app_name, question, None, None))
    
    return new_luis
        
def read_for_qna(file_name, dispatcher):
    lines = read_file(file_name)
    qna = None
    new_qnas = []
    new_luis = []

    for line in lines:
        if not not ''.join(line.split()):
            data = line.split(SPLIT_DATA)

            if len(data) >= 2:
                attrib = data[0].strip()
                value  = data[1].strip()

            if match(attrib, 'app_name'):
                if qna is not None and qna.complete():
                    new_qnas.append(qna)
                    new_luis = new_luis + luis_for_qna(qna.app_name, qna.questions, dispatcher)
                    qna = None

                credential = find_credential(value, read_credentials())
                qna = QnA(credential, value, None, None)

            if qna is not None:
                if match(attrib, 'questions'):
                    qna.questions = get_additional(value)
                if match(attrib, 'answer'):
                    qna.answer = value

    if qna is not None and qna.complete():
        new_qnas.append(qna)

    return new_qnas + new_luis

def read_for_luis(file_name):
    lines = read_file(file_name)
    luis = None
    new_luis = []

    for line in lines:
        if not not ''.join(line.split()):
            data = line.split(SPLIT_DATA)

            if len(data) >= 2:
                attrib = data[0].strip()
                value  = data[1].strip()

                if match(attrib, 'app_name'):
                    if luis is not None and luis.complete():
                        new_luis.append(luis)
                        luis = None

                    credential = find_credential(value, read_credentials())
                    luis = Luis(credential, value, None, None, None)

                if luis is not None:
                    if match(attrib, 'question'):
                        luis.question = value
                    if match(attrib, 'labels'):
                        luis.labels = get_additional(value)
                    if match(attrib, 'values'):
                        luis.values = get_additional(value)

    if luis is not None and luis.complete():
        new_luis.append(luis)

    return new_luis