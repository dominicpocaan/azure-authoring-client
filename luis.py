from azure.cognitiveservices.language.luis.authoring import LUISAuthoringClient
from msrest.authentication import CognitiveServicesCredentials

import datetime, json, os, time




class Luis:
    
    def __init__(self, credential, question, labels, values):
        self.credential = credential
        self.question   = question
        self.labels     = labels
        self.values     = values

    def complete(self):
        req_list = ['question']

        attributes = self.__dict__

        for attrib in attributes.values():
            return False if attrib is None else True

    @static
    def create_utterance(self, intent, utterance, *labels):
        text = utterance.lower()

        def label(name, value):
            value = value.lower()
            start = text.index(value)

            return dict(entity_name=name, start_char_index=start,
                        end_char_index=start + len(value))

        return dict(text=text, intent_name=intent,
                    entity_labels=[label(n, v) for (n, v) in labels])

    def update(self, new_utterances):
        endpoint = "https://{}.api.cognitive.microsoft.com".format(self.credential.region)
        client = LUISAuthoringClient(endpoint, CognitiveServicesCredentials(self.credential.key))

        utterances = new_utterances

        client.examples.batch(self.credential.app_id, self.credential.version, utterances)
        print("{} utterance(s) added.".format(len(utterances)))

    def __str__(self):
        return '{}, {}, {}, {}, {}'.format(self.name, self.version, self.key, self.region, self.app_id)
