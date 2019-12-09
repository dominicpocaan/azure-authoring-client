from qna import QnA
from luis import Luis
from  credential import Credential


class Parser:

    @staticmethod
    def read_file(file_name):
        try:
            lines = []

            with open(file_name, 'r') as file:
                for line in file:
                    lines.append(line.rstrip('\n'))

            return lines
        except IOError:
            print('Error: File {} file does not exist !!!'.format(file_name))

    @staticmethod
    def read_credentials():
        lines = Parser.read_file('credentials.txt')
        credential = None
        new_credentials = []

        for i in range(len(lines)):
            if len(''.join(lines[i].split())) > 0:
                data = lines[i].split(':')

                if len(data) >= 2:
                    if data[0].lower().strip() == 'type':
                        if credential != None:
                            if credential.complete():
                                new_credentials.append(credential)
                                credential = None
                            else:
                                credential = None
                        
                    credential = Credential(None, None, None, None, None, None, None)

                if credential != None:
                    if data[0].lower().strip() == 'name':
                        credential.name = data[1].strip()
                    elif data[0].lower().strip() == 'version':
                        credential.version = data[1].strip()
                    elif data[0].lower().strip() == 'key':
                        credential.key = data[1].strip()
                    elif data[0].lower().strip() == 'region':
                        credential.region = data[1].strip()
                    elif data[0].lower().strip() == 'host':
                        credential.host = '{}:{}'.format(data[1].strip(), data[2].strip())
                    elif data[0].lower().strip() == 'id':
                        credential.app_id = data[1].strip()
        
        if credential != None:
            if credential.complete():
                new_credentials.append(credential)
                credential = None
        
        return new_credentials