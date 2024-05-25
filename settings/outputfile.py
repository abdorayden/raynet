#from config import extentions
import os

class ERROR_Out_Put(Exception):
    pass

class _Html_Out_File :
    pass

class _Json_Out_File :
    pass

class _Txt_Out_File :
    pass

class _Toml_Out_File :
    pass

class Out_Put :

    def __init__(self , extention):
        self.extention = extention
        if not self.check():
            raise ERROR_Out_Put

    def check(self):
        return self.extention in self.extentions

