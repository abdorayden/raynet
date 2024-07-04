"""
    this is part of raynet tool
"""

from settings.config import osi_map

class Connector(object):
    def __init__(
            self , 
            osi , 
            protocole
        ) -> None :
        self.osi = osi
        self.protocole = protocole

    def connect(self):
        pass




