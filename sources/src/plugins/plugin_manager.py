import imp

#TODO Write documentation for this classes

class PluginManager:
    def __init__(self):
        pass
    
    def load_module(self,p_name):
        f, filename, description = imp.find_module(p_name)
        return imp.load_module('plugins.'+p_name,f,filename,description)


class PluginDatabaseInit:
    CONN_OBJ = None
    CURSOR = None

    def __init__(self,p_conn_obj):
        self.CONN_OBJ = p_conn_obj
        self.CURSOR = self.CONN_OBJ.get_connection().cursor()

    def __del__(self):
        self.CURSOR.close()
        pass

class PluginMongoInit:
    CONN_OBJ = None

    def __init__(self,p_conn_obj):
        self.CONN_OBJ = p_conn_obj

    def __del__(self):
        pass
