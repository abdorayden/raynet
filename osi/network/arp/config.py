"""
    part of arp class of netmap
"""
from uuid import getnode , UUID
from binascii import unhexlify
from socket import (
            gethostname,
            gethostbyname,
            inet_aton
        )

HARDWARE_TYPE = 0x0001
PROTOCOLE_TYPE = 0x0800
HARDWARE_ADDRESS_LENGTH = 0x06
PROTOCOLE_ADDRESS_LENGTH = 0x04
OPERATION_DATA_REQ = 0x0001
OPERATION_DATA_REP = 0x0002
#
def _local_mac():
    mac = UUID(int=getnode()).hex[-12:]
    return ':'.join(mac[i:i+2] for i in range(0, 12, 2))

_local_ip = inet_aton(gethostbyname(gethostname()))

TARGET_ADDRESS = unhexlify("00:00:00:00:00:00:".replace(":",""))
