import sys
import json
from config import *
sys.path.insert(0, './plugins') # drop when switching to uWSGI. Only for DEBUG!!!!
from core.classes.database_class import dbInit
from core.classes.mongo_class import mongoInit
from core.classes.session_writer_class import SessionWriter

import plugins

#TODO: Write documentation for request parser class
#TODO: Write comments for all classes and methods

class RequestParam():
    requestType = None
    contentType = None
    requestData = None
    sessionData = None

class RequestParser():
    QUERY = None
    ERROR = 0
    REQUEST = RequestParam()
    PLUGIN = None
    MONGO_CONN = None
    PG_CONN = None
    SESSION = None
    
    def __init__(self,p_query):
        try:
            self.QUERY = json.loads(p_query)
            self._parse()
        except:
            self.ERROR = 101
            return
        
        try:
            self._infraConnection()
        except:
            self.ERROR = 111
            return

        if self.ERROR not in (101,100):
            self._sessionCheck()
    
    def _parse(self):
        #TODO logical parse incoming params
        self.REQUEST.requestType = self.QUERY['requestType']
        self.REQUEST.contentType = self.QUERY['contentType']
        self.REQUEST.requestData = self.QUERY['requestData']
        self.REQUEST.sessionData = self.QUERY['sessionData']

    def _infraConnection(self):
        self.MONGO_CONN = mongoInit(MONGO_HOST)
        self.PG_CONN = dbInit('dbname=%s host=%s port=%s user=%s password=%s' % (PG_DB,PG_HOST,PG_PORT,PG_USER,PG_PASS))

    def _sessionCheck(self):
        self.SESSION = SessionWriter(self.MONGO_CONN)
        if self.REQUEST.requestType != 100 \
            or (self.REQUEST.requestType == 100 and self.REQUEST.contentType == 120):
            data = self.SESSION.check_session(self.REQUEST.sessionData['UUID'],self.REQUEST.sessionData['tKey'])
            if data == 132:
                self.ERROR = data
        return

    def distribute(self):
        if self.ERROR != 0:
            return

        if self.REQUEST.requestType == 0:
            print("multi requests")

        elif self.REQUEST.requestType == 100:
            plug_link = plugins.Manager.load_module('authorization')
            self.PLUGIN = plug_link.Plugin(self.MONGO_CONN,self.PG_CONN,self.REQUEST.requestData,self.SESSION)
            self.PLUGIN.Start(self.REQUEST.contentType)

#        elif self.REQUEST.requestType == 200:
#            plug_link = plugins.Manager.load_module('budget')
#            self.PLUGIN = plug_link.Plugin(self.MONGO_CONN,self.PG_CONN,self.REQUEST.requestData)
#            if self.PLUGIN.check_request() == 1:
#                self.ERROR = self.PLUGIN.ERROR
#                return
#            self.PLUGIN.Start(self.REQUEST.contentType)

#        elif self.REQUEST.requestType == 300:
#            plug_link = plugins.Manager.load_module('dictionary')
#            self.PLUGIN = plug_link.Plugin(self.MONGO_CONN,self.PG_CONN,self.REQUEST.requestData)
#            if self.PLUGIN.check_request() == 1:
#                self.ERROR = self.PLUGIN.ERROR
#                return
#            self.PLUGIN.Start(self.REQUEST.contentType)

        else:
            self.ERROR = 110
        
    def output(self):
        returns = {}
        if self.ERROR == 0:
            returns = self.PLUGIN.gen_output()
        else:
            returns['responseType'] = 400
            returns['responseData'] = ({ 'error' : self.ERROR })
        return json.dumps(returns)
    
    def __del__(self):
        pass


if __name__ == '__main__':

    data = {}
    data['requestType'] = 100
    data['contentType'] = 110
    data['requestData'] = { }
    data['requestData'] = { "auth_type" : 1, "productId" : 1, "user_email" : "miha@miha20" ,"user_password" : "test_test20" }
#    data['sessionData'] = { "UUID" : "86f3164dc4b9468a29c703d7a4fd3e3b","tKey" : "d02ddbc204f268acc55bbadbe3979c550d73e7a0" }
    data['sessionData'] = { "UUID" : None ,"tKey" : None }

    print(json.dumps(data))

#    data = '{"requestType":100,"contentType":100,"requestData":{"productId":1,"user_email":"miha@miha8","user_password":"test_test88"}}'
#    data = '''{"requestType":200,
#               "contentType":100,
#               "requestData":{"UUID":"6daf35b89d3e9e0179efd9b1785e9dc5",
#                              "tKey":"7779e78f91fb45b512be6f8a8d8750b1d2b6200d",
#                              "value":"2.70",
#                              "category":"14",
#                              "description":"test from .py file",
#                              "productId":1,
#                              "submitTs":"1345213728.092619"}}'''

#    data = '''{"requestType":300,
#               "contentType":100,
#               "requestData":{"UUID":"7cfff97fbf2bf1a9dce181386d8b80b6",
#                              "tKey":"865b64328c24917159f8d16fbb5919466e53557b",
#                              "category_name":"load manual55"}}'''

    result = RequestParser(json.dumps(data))
    result.distribute()
    print(result.output())


