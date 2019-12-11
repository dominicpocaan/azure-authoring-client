from azure.cognitiveservices.knowledge.qnamaker import QnAMakerClient
from azure.cognitiveservices.knowledge.qnamaker.models import QnADTO, MetadataDTO, CreateKbDTO, OperationStateType, UpdateKbOperationDTO, UpdateKbOperationDTOAdd

from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient

from msrest.authentication import CognitiveServicesCredentials

import datetime, json, os, time




class QnA:
    
    def __init__(self, credential, questions, answer):
        self.credential = credential
        self.questions  = questions
        self.answer     = answer

    def complete_credentials(self):
        req_list = ['questions', 'answer']
        attributes = self.__dict__

        for attrib in attributes.values():
            return False if attrib is None else True
    
    def publish(self):
        self.credential.client.knowledgebase.publish(kb_id = self.credential.app_id)

    def update(self):
        update_kb = UpdateKbOperationDTO( 
            add = UpdateKbOperationDTOAdd(
                qna_list = [QnADTO(questions = self.questions, answer = self.answer)]
            )
        )
        self.credential.client.knowledgebase.update(kb_id = self.credential.app_id, 
                                                    update_kb = update_kb)

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.name, self.key, self.host, self.app_id)



class Luis:
    REQ_LIST = ['question']

    def __init__(self, credential, question, labels, values):
        self.credential = credential
        self.question   = question
        self.labels     = labels
        self.values     = values

    def complete(self):
        attributes = self.__dict__

        for req in Luis.REQ_LIST:
            if attributes[req] is None:
                return False
        return True

    @staticmethod
    def create_utterance(intent, utterance, *labels):
        text = utterance.lower()

        def label(name, value):
            value = value.lower()
            start = text.index(value)

            return dict(entity_name = name, start_char_index = start,
                        end_char_index = start + len(value))

        return dict(text = text, intent_name = intent,
                    entity_labels = [label(n, v) for (n, v) in labels])

    def publish(self):
        self.credential.client.train.train_version(self.credential.app_id, self.credentialapp_version)
        self.credential.client.apps.publish(self.credential.app_id, self.credential.app_version, 
                                            is_staging=True)

    def update(self, utterance):
        self.credential.client.examples.batch(self.credential.app_id, self.credentialapp_version, 
                                              utterance)

    def __str__(self):
        return '{}, {}, {}, {}, {}'.format(self.name, self.version, self.key, 
                                           self.region, self.app_id)