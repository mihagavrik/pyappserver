from core.classes.sessions_class import Session
from config import MONGO_SESSION_DB, MONGO_SESSION_COLLECTION, SESSION_LIFETIME
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

    def _update_tKey(self):
        self.SESSION_DATA["data"]["tKey"] = self.get_urid()
        self.MONGO_COLL.update({"_id" : self.get_sid()},{"$set" : {"data.tKey" : self.SESSION_DATA["data"]["tKey"]}})

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

    def check_session(self,p_sid,p_tKey):
        data = self.MONGO_COLL.find( {"_id" : p_sid, "data.tKey" : p_tKey, "updated":{ "$gt": time.time() - SESSION_LIFETIME}, "is_closed" : 0 })
        if data.count() == 0:
            return 132
        self.set_sid(p_sid)
        self.SESSION_DATA = data[0]
        return self.SESSION_DATA["data"]

    def is_session_enable(self,p_user_id):
        data = self.MONGO_COLL.find({"data.userId":p_user_id,"updated":{ "$gt": time.time() - SESSION_LIFETIME }, "is_closed" : {"$exists" : 0} })
        if data.count() == 0:
            return 130
        self.SESSION_DATA = data[0]
        self.set_sid(self.SESSION_DATA["_id"])
        self._update_tKey()
        return self.get_sid()

    def close_session(self):
        self.MONGO_COLL.update({ "_id" : self.SID },{"$set" : { "is_closed" : 1 }})

    def set_session(self):
        pass

    def __del__(self):
        if self.SID is not None:
            self.MONGO_COLL.update({"_id" : self.SID},{"$set" : {"updated" : time.time() }})
