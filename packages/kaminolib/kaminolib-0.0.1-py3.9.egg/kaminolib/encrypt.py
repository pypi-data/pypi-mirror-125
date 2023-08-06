import hashlib

class Encrypt:
    @staticmethod
    def md5(raw):
        if isinstance(raw,bytes):
            return hashlib.md5(raw).hexdigest()
        if isinstance(raw,str):
            return hashlib.md5(raw.encode('utf8')).hexdigest()
        
        raise Exception("not support type")