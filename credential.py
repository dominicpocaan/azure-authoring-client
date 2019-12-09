


class Credential:

    QNA_LIST = ['name', 'key', 'host', 'app_id']
    LUIS_LIST = ['name', 'version', 'key', 'region', 'app_id']

    def __init__(self, app_type, app_name, app_version, app_key, 
                 app_region, app_host, app_id):
        self.app_type    = app_type
        self.app_name    = app_name
        self.app_version = app_version
        self.app_key     = app_key
        self.app_region  = app_region 
        self.app_host    = app_host
        self.app_id      = app_id

    def complete(self):
        req_list = None

        try:
            app_type = ''.join(self.app_type.split())
            req_list = self.QNA_LIST if app_type is 'qna' else self.LUIS_LIST
        except:
            print('Error: Invalod application type !!!')

        attributes = self.__dict__
        for req in req_list:
            return False if attributes[req] is None else True

    def __str__(self):
        app_type = ''.join(self.app_type.split())

        if app_type == 'qna':
            info = ''' 
                    QnA Name: {}
                    QnA Key:  {}
                    QnA Host: {}
                    QnA ID:   {} 
                   '''
            info = info.format(self.app_name, self.app_key, 
                               self.app_host, self.app_id)
            return info.replace('\t', '').replace(' ', '')
        elif app_type == 'luis':
            info = ''' 
                    LUIS Name:    {}
                    LUIS Version: {}
                    LUIS Key:     {}
                    LUIS Region:  {}
                    LUIS ID:      {}
                   '''

            info = info.format(self.app_name, self.app_version, 
                               self.app_key, self.app_region, 
                               self.app_id)
            return info.replace('\t', '').replace(' ', '')
        else:
            info = '{}, {}, {}, {}, {}, {}, {}' 
            return info.format(self.app_type, self.app_name, 
                               self.app_version, self.app_key, 
                               self.app_region, self.app_host, 
                               self.app_id)