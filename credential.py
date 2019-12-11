from azure.cognitiveservices.knowledge.qnamaker import QnAMakerClient
from azure.cognitiveservices.knowledge.qnamaker.models import QnADTO, MetadataDTO, CreateKbDTO, OperationStateType, UpdateKbOperationDTO, UpdateKbOperationDTOAdd

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient

from msrest.authentication import CognitiveServicesCredentials



class Credential:

    QNA_LIST = ['app_name', 'app_key', 'app_host', 'app_id']
    LUIS_LIST = ['app_name', 'app_version', 'app_key', 'app_region', 'app_id']

    def __init__(self, app_type, app_name, app_version, 
                 app_key, app_region, app_host, app_id):
        self.app_type    = app_type
        self.app_name    = app_name
        self.app_version = app_version
        self.app_key     = app_key
        self.app_region  = app_region 
        self.app_host    = app_host
        self.app_id      = app_id
        self.app_client  = self.create_client()
        
    def create_client(self):
        qna_client  = QnAMakerClient(endpoint = self.host, 
        credentials = CognitiveServicesCredentials(self.key))
        endpoint    = f'https://{ self.region }.api.cognitive.microsoft.com'
        luis_client = LUISAuthoringClient(endpoint, 
        CognitiveServicesCredentials(self.key))

        app_type    = ''.join(self.app_type.split()).lower()
        return qna_client if app_type == 'qna' else luis_client

    def complete(self):
        req_list = None

        try:
            app_type = ''.join(self.app_type.split()).lower()
            req_list = self.QNA_LIST if app_type == 'qna' else self.LUIS_LIST
        except:
            print('Error: Invalid application type !!!')

        attributes = self.__dict__

        for req in req_list:
            if attributes[req] is None:
                return False
        return True

    def __str__(self):
        app_type = ''.join(self.app_type.split()).lower()

        if app_type == 'qna':
            info = ''' QnA Name: {}
                       QnA Key:  {}
                       QnA Host: {}
                       QnA ID:   {} '''
            info = info.format(self.app_name, self.app_key, 
                               self.app_host, self.app_id)
            return info.replace('\t', '').replace(' ', '')
        elif app_type == 'luis':
            info = ''' LUIS Name:    {}
                       LUIS Version: {}
                       LUIS Key:     {}
                       LUIS Region:  {}
                       LUIS ID:      {} '''

            info = info.format(self.app_name, self.app_version, 
                               self.app_key, self.app_region, 
                               self.app_id)
            return info.replace('\t', '').replace(' ', '')
        else:
            info = '{}, {}, {}, {}, {}, {}, {}' 
            return info.format(self.app_type, self.app_name, self.app_version, 
                               self.app_key, self.app_region, self.app_host, 
                               self.app_id)