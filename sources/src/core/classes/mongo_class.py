from pymongo import Connection

class mongoInit:
    CONN = None
    
    def __init__(self,p_host):
        self.CONN = Connection(p_host)
    
    def __del__(self):
        self.CONN.close()
    
    def get_connection(self):
        return self.CONN
