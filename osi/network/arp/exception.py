#!/usr/bin/env python3

class ARPError(Exception):
    pass

class ConnectionTimeout(ARPError):
    pass

class Invalid_IP_Address(ConnectionTimeout):
    pass

class Address_Block_Unkonw(Invalid_IP_Address):
    pass

class IP_Error(Address_Block_Unkonw):
    pass
