from azure.cognitiveservices.knowledge.qnamaker import QnAMakerClient
from azure.cognitiveservices.knowledge.qnamaker.models import QnADTO, MetadataDTO, CreateKbDTO, OperationStateType, UpdateKbOperationDTO, UpdateKbOperationDTOAdd
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

    @staticmethod
    def monitor_operation(client, operation):
        for i in range(20):
            if operation.operation_state in [OperationStateType.not_started, OperationStateType.running]:
                print("Waiting for operation: {} to complete.".format(operation.operation_id))
                operation = client.operations.get_details(operation_id=operation.operation_id)
            else:
                break
        if operation.operation_state != OperationStateType.succeeded:
            raise Exception("Operation {} failed to complete.".format(operation.operation_id))
        return operation

    def update(self):
        client = QnAMakerClient(endpoint = self.credential.host, credentials = CognitiveServicesCredentials(self.credential.key))

        update_kb_operation_dto = UpdateKbOperationDTO(
            add = UpdateKbOperationDTOAdd(
                qna_list = [
                    QnADTO(questions = self.questions, answer = self.answer)
                ]
            )
        )

        update_op = client.knowledgebase.update(kb_id = self.credential.app_id, update_kb = update_kb_operation_dto)
        monitor_operation(client = client, operation = update_op)

        client.knowledgebase.publish(kb_id = self.credential.app_id)

        print('New data added in {}.'.format(self.credential.name))
        print('Question/s: ')

        for q in range(len(self.questions)):
            print(self.questions[q])

        print('Answer: {}'.format(self.answer))

    def __str__(self):
        return '{}, {}, {}, {}'.format(self.name, self.key, self.host, self.app_id)