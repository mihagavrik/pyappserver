from core.classes.sessions_class import Session
from config import MONGO_SESSION_DB, MONGO_SESSION_COLLECTION
import time

class SessionWriter(Session):
    MONGO_OBJ = None
    MONGO_COLL = None
    SESSION_DATA = None

    def __init__(self,p_mongo_obj):
        self.MONGO_OBJ = p_mongo_obj
        self.MONGO_COLL = self.MONGO_OBJ.get_connection()[MONGO_SESSION_DB][MONGO_SESSION_COLLECTION]
    
    def _empty_session(self):
        self.SESSION_DATA = { "_id" : self.SID, "created" : time.time(), "updated" : time.time(), "data" : {} }

    def create(self, p_user_id):
        self.get_sid()
        self._empty_session()
        self.SESSION_DATA["data"] = {"userId" : p_user_id, "tKey" : self.get_urid()}
        self.MONGO_COLL.insert(self.SESSION_DATA)

    def get_session(self,p_sid):
        self.set_sid(p_sid)
        data = self.MONGO_COLL.find( { "_id" : self.SID } )
        if data.count() == 0:
            return 130
        return data[0]

    def __del__(self):
        pass
