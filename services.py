from azure.cognitiveservices.knowledge.qnamaker import QnAMakerClient
from azure.cognitiveservices.knowledge.qnamaker.models import QnADTO, MetadataDTO, CreateKbDTO, OperationStateType, UpdateKbOperationDTO, UpdateKbOperationDTOAdd

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient

from msrest.authentication import CognitiveServicesCredentials

import datetime, json, os, time



class QnA:
    REQ_LIST = ['questions', 'answer']

    def __init__(self, credential, app_name, questions, answer):
        self.credential = credential
        self.app_name   = app_name
        self.questions  = questions
        self.answer     = answer

    def complete(self):
        attributes = self.__dict__

        for req in QnA.REQ_LIST:
            if attributes[req] is None:
                return False

        return True
    
    def publish(self):
        client = QnAMakerClient(endpoint = self.credential.app_host, 
        credentials = CognitiveServicesCredentials(self.credential.app_key))
        client.knowledgebase.publish(kb_id = self.credential.app_id)

    def update(self):
        client = QnAMakerClient(endpoint = self.credential.app_host, 
        credentials = CognitiveServicesCredentials(self.credential.app_key))
        update_kb_operation_dto = UpdateKbOperationDTO( 
            add = UpdateKbOperationDTOAdd(
                qna_list = [QnADTO(questions = self.questions, answer = self.answer)]
            )
        )
        client.knowledgebase.update(kb_id = self.credential.app_id, 
                                    update_kb = update_kb_operation_dto)
        time.sleep(5)

    def __str__(self):
        return '{}, {}, {}'.format(self.app_name, self.questions, self.answer)



class Luis:
    REQ_LIST = ['question']

    def __init__(self, credential, app_name, question, labels, values):
        self.credential = credential
        self.app_name   = app_name
        self.question   = question
        self.labels     = labels
        self.values     = values

    def complete(self):
        attributes = self.__dict__

        flag_1 = False
        flag_2 = False

        for req in Luis.REQ_LIST:
            if attributes[req] is None:
                return False
            else:
                flag_1 = True

        if self.labels is not None and self.values is not None:
            if len(self.labels) == len(self.values):
                flag_2 = True
        else:
            flag_2 = True

        return flag_1 and flag_2

    def create_labels(self):
        new_labels = ()
        for i in range(len(self.labels)):
            temp = list(new_labels)
            temp.append((self.labels[i].strip(), self.values[i].strip()))
            new_labels = tuple(temp)

        return new_labels

    def create_utterance(self, labels):
        text = self.question.lower()

        def label(name, value):
            value = value.lower()
            start = text.index(value)

            return dict(entity_name = name, start_char_index = start,
                        end_char_index = start + len(value))

        return dict(text = text, intent_name = self.app_name,
                    entity_labels = [label(n, v) for (n, v) in labels])

    def publish(self):
        endpoint = f'https://{ self.credential.app_region }.api.cognitive.microsoft.com'
        client = LUISAuthoringClient(endpoint, CognitiveServicesCredentials(self.credential.app_key))
        client.train.train_version(self.credential.app_id, self.credential.app_version)
        client.apps.publish(self.credential.app_id, self.credential.app_version, is_staging=True)

    def update(self):
        endpoint = f'https://{ self.credential.app_region }.api.cognitive.microsoft.com'
        client = LUISAuthoringClient(endpoint, CognitiveServicesCredentials(self.credential.app_key))
        utterance = None

        if self.labels is not None and self.values is not None:
            utterance = self.create_utterance(self.create_labels())
        else:
            labels = ()
            utterance = self.create_utterance(labels)

        client.examples.batch(self.credential.app_id, self.credential.app_version, 
                                              [utterance])
        time.sleep(5)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.app_name, self.question, 
                                       self.labels, self.values)