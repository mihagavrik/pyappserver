from core.classes.generator_class import GeneratorUUID

class Session:
    
    SID = None
    URID = None
    generator = GeneratorUUID()
    
    def __init__(self):
        return
    
    def __del__(self):
        return

    def _gen_sid(self):
        return self.generator.generate_uuid()
        
    def _gen_urid(self):
        return self.generator.generate_urid()

    def set_sid(self,p_sid):
        if p_sid == '' or p_sid == None:
            return 0
        self.SID = p_sid
        return 1
    
    def get_sid(self):
        if self.SID == None:
            self.SID = self._gen_sid()
        return self.SID
    
    def get_urid(self):
        if self.URID == None:
            self.URID = self._gen_urid()
        return self.URID



if __name__ == '__main__':
    
    session = Session()
    if session.set_sid(''):
        print(session.get_sid())
    else:
        print("Session is not set")
    
    print(session.get_sid())
