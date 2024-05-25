"""
    part of arp class of netmap
"""
# standerd packages
from struct import pack
import sys
import socket
import os

#_path = os.getcwd().split("/")
#_path.remove(os.getcwd().split("/")[-1])
#sys.path.append("/"+"/".join(i for i in _path if i))

try:
    # configuration
    from osi.network.arp.config import HARDWARE_TYPE
    from osi.network.arp.config import PROTOCOLE_TYPE
    from osi.network.arp.config import HARDWARE_ADDRESS_LENGTH
    from osi.network.arp.config import PROTOCOLE_ADDRESS_LENGTH
    from osi.network.arp.config import OPERATION_DATA_REQ
    from osi.network.arp.config import OPERATION_DATA_REP
    from osi.network.arp.config import _local_mac
    from osi.network.arp.config import _local_ip
    from osi.network.arp.config import TARGET_ADDRESS
    ########################################
    from osi.network.ip4.ipv4 import IP_Address
    #import ipv4
    from settings.config import debug
    from settings.config import error

except ModuleNotFoundError as err:
    error(err)
    exit(1)

# exception
from osi.network.arp.exception import ARPError
from osi.network.arp.exception import ConnectionTimeout
from osi.network.arp.exception import Invalid_IP_Address
from osi.network.arp.exception import Address_Block_Unkonw
from osi.network.arp.exception import IP_Error

# methods
__M_OP__ = [
        "REQ",
        "REP"
        ]
# values
__OP__ = {
    "REQ" : OPERATION_DATA_REQ,
    "REP" : OPERATION_DATA_REP
}

"""
    making arp packet
"""
def _make_arp_packet(
        operation : str       = None,
        src_mac : str       = _local_mac(),
        src_ip  : str       = None ,
        dest_mac  : str       = TARGET_ADDRESS,
        dest_ip   : str       = None
                 ) -> bytes :

    """
        checking opirations
    """
    if src_ip is None :
        src_ip = _local_ip
    else :
        src_ip = socket.inet_aton(src_ip)


    if dest_ip is None:
        raise ARPError("destinatio IP is None")
    dest_ip_binary = socket.inet_aton(dest_ip)

    if operation is None or operation not in __M_OP__ :
        raise ARPError("Invalid method")

    op = __OP__[operation]
    d_ip = _dest_ip(dest_ip)
    if dest_ip is None :
        raise ARPError("Invalid target ip address")

    return b"".join(
                [
                    pack("!H"  , HARDWARE_TYPE),
                    pack( "!H" , PROTOCOLE_TYPE),
                    pack( "!B" , HARDWARE_ADDRESS_LENGTH),
                    pack( "!B" , PROTOCOLE_ADDRESS_LENGTH),
                    pack( "!H" , op),
                    pack( "!6s", src_mac),
                    pack( "!4s", src_ip),
                    pack( "!6s", dest_mac),
                    pack( "!4s", dest_ip_binary),
                ]
                )



class ARP(object):
    def __init__(
            self , 
            # in ipv4 module get interface name if its None
            interface : str = None,
            operation : str = None, 
            src_ip : str = None, 
            src_mac : str = None, 
            dest_ip : str = None, 
            dest_mac = TARGET_ADDRESS,
            debug = False
        ) -> None:
        try :
            self.interface = interface or IP_Address(src_ip).iface
        except IP_Error:
            self.interface = IP_Address(socket.gethostbyname(socket.gethostname()))

        self.op = operation or "REQ"  
        self.src_mac = src_mac or _local_mac()
        self.dest_mac = dest_mac
        """
            it will raise if it's error here
        """
        self.packet = _make_arp_packet(self.op , self.src_mac , src_ip , self.dest_mac , dest_ip)
        self.rec_packet = None
        self.debug = debug
        if self.debug:
            debug("Debug Enable")



    def connection(self):
        if self.debug:
            debug(f"arp operation : {self.op}")
            debug(f"packet : {self.packet}")

        with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003)) as sock:
            sock.bind((self.interface, 0))

            if self.debug:
                debug(f"bind on {self.interface} interface")

            
            eth_header = b"".join(
                    [
                        pack("!6s" , self.dest_mac),
                        pack("6s", self.src_mac),
                        pack("H",  0x0806)
                    ]
                )
            if self.debug:
                debug(f"creating arp header {eth_header}")

            packet = eth_header + self.packet

            # Send packet
            sock.send(packet)
            if self.debug:
                debug(f"sending packet : {packet}")

            # Listen for ARP reply
            while True:
                received_packet, addr = sock.recvfrom(65535)
                if self.debug:
                    debug(f"reciving packet : {received_packet}")
                eth_type, = struct.unpack("!H", received_packet[12:14])
                if eth_type == 0x0806:  # ARP packet
                    arp_opcode, = struct.unpack("!H", received_packet[20:22])
                    if arp_opcode == 0x0002:  # ARP reply
                        #return (self.extract_header(received_packet))
                        self.received_packet = received_packet
                        break
        return True
    def check(self):
        return self.rec_packet is not None

#ARP(operation = "REQ" , dest_ip = "192.168.0.200").connection()
