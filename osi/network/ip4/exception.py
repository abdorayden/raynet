"""
    IP Adress exception
"""
class IP_Error(Exception):
    pass

class Invalid_IP_Address(IP_Error):
    pass

class Address_Block_Unkonw(Invalid_IP_Address):
    pass
