import psycopg2



class dbInit:
    
    CONN = None
    
    def __init__(self,p_connStr):
        self.CONN = psycopg2.connect(p_connStr)
    
    def __del__(self):
        self.CONN.close()
    
    def set_autocommit(self):
        self.CONN.autocommit = True
            
    def get_connection(self):
        return self.CONN



if __name__ == '__main__':
    
    DB = dbInit('dbname=app_base host=192.168.120.162 port=9999 user=app_server password=app_server')
