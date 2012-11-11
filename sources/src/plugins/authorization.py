from core.classes.generator_class import PasswordHash
#from core.classes.session_writer_class import SessionWriter

#TODO: Write documentation for plugins method

class RequestData:
    auth_type = None
    user_email = None
    user_password = None
    productId = None

class PluginDatabase:
    CONN_OBJ = None
    CURSOR = None
    
    def __init__(self,p_conn_obj):
        self.CONN_OBJ = p_conn_obj
        self.CONN_OBJ.set_autocommit()
        self.CURSOR = self.CONN_OBJ.get_connection().cursor()
    
    def register_new_customer(self,p_request_obj):
        if p_request_obj.auth_type == 1:
            self.CURSOR.callproc('customer.register_user',[p_request_obj.auth_type,
                                                           p_request_obj.user_email,
                                                           p_request_obj.user_password])
            return self.CURSOR.fetchone()
    
    def login_customer(self,p_request_obj):
        if p_request_obj.auth_type == 1:
            self.CURSOR.callproc('customer.login',[p_request_obj.auth_type,
                                                   p_request_obj.user_email,
                                                   p_request_obj.user_password])
            return self.CURSOR.fetchone()
    
    def __del__(self):
        self.CURSOR.close()
        pass


class PluginMongo:
    CONN_OBJ = None
    
    def __init__(self,p_conn_obj):
        self.CONN_OBJ = p_conn_obj
    
    def __del__(self):
        pass

class Plugin:
    MONGO_CONN = None
    PG_CONN = None
    REQUEST_DATA = RequestData()
    ERROR = 0
    session = None
    contentType = None
    global_request = None
    
    def __init__(self,p_mongo_conn,p_pg_conn,p_request_data,p_session_obj):
        self.MONGO_CONN = PluginMongo(p_mongo_conn)
        self.PG_CONN = PluginDatabase(p_pg_conn)
        self.session = p_session_obj
        self.global_request = p_request_data

    def _content_data(self):
        if self.contentType == 100 or self.contentType == 110:
            self.REQUEST_DATA.auth_type = self.global_request['auth_type']
            self.REQUEST_DATA.productId = self.global_request['productId']

            if self.REQUEST_DATA.auth_type == 1:
                self.REQUEST_DATA.user_email = self.global_request['user_email']
                self.REQUEST_DATA.user_password = PasswordHash(self.global_request['user_password']).get_sha1()

        if self.contentType == 120:
            pass

    def login(self):
        user_id,err = self.PG_CONN.login_customer(self.REQUEST_DATA)
        if err == 0 and self.session.is_session_enable(user_id) != 132:
            self.session.create(user_id)
        else:
            self.ERROR = '%s' % err
    
    def register(self):
        user_id,err = self.PG_CONN.register_new_customer(self.REQUEST_DATA)
        if err == 0:
            self.session.create(user_id)
        else:
            self.ERROR = '%s' % err
    
    def logout(self):
        self.session.close_session()
        self.ERROR = 133

    def Start(self,p_content_type):
        self.contentType = p_content_type
        self._content_data()

        if self.contentType == 100:
            self.register()

        elif self.contentType == 110:
            self.login()

        elif self.contentType == 120:
            self.logout()

        else:
            self.ERROR = 120

        
    def gen_output(self):
        returns = {}
        if self.ERROR == 0:
            returns['responseType'] = 100
            returns['contentType'] = self.contentType
            returns['responseData'] = ({ 'UUID' : self.session.get_sid(), 'tKey' : self.session.get_urid() })
        else:
            returns['responseType'] = 400
            returns['responseData'] = ({ 'error' : self.ERROR })

        return returns
