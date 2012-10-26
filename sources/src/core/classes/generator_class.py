import os
import time
import hashlib


class GeneratorUUID:
    
    def __init__(self):
        return
    
    def _uniq_str(self):
        STR = str(time.time()) + str(os.urandom(5))
        return STR.encode('utf-8')
    
    def generate_uuid(self):
        return hashlib.md5(self._uniq_str()).hexdigest()
    
    def generate_urid(self):
        return hashlib.sha1(self._uniq_str()).hexdigest()

    def get_uuid_urid(self):
        return self.generate_uuid(), self.generate_urid()


class PasswordHash:
    STR = None
    def __init__(self,p_str):
        self.STR = p_str.encode('utf-8')
    
    def get_sha1(self):
        return hashlib.sha1(self.STR).hexdigest()



if __name__ == '__main__':
    gen=GeneratorUUID()
    
    for i in range(30):
        print(gen.get_uuid_urid())

        
