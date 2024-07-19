"""
    part of arp class of netmap
"""
# standerd packages
from struct import pack , unpack
import sys
import binascii
import socket
import os

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

    from osi.network.ip4.ipv4 import IP_Address
    from settings.config import debug
    from settings.config import error

except ModuleNotFoundError as err:
    error(err)
    exit(1)

# exception
from osi.network.arp.exception import ARPError
from osi.network.arp.exception import ConnectionTimeout
from osi.network.ip4.exception import Invalid_IP_Address
from osi.network.ip4.exception import Address_Block_Unkonw
from osi.network.ip4.exception import IP_Error

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
    #if src_ip is None :
    #    src_ip = _local_ip
    #else :
    #    src_ip = socket.inet_aton(src_ip)
    src_ip = socket.inet_aton("192.168.0.125")
    debug(msg = f"local ip is : {src_ip}")

    if dest_ip is None:
        raise ARPError("destinatio IP is None")
    dest_ip_binary = socket.inet_aton(dest_ip)

    debug(msg = f"destination ip is : {dest_ip_binary}")
    if operation is None or operation not in __M_OP__ :
        raise ARPError("Invalid method")

    op = __OP__[operation]
    if dest_ip is None :
        raise ARPError("Invalid target ip address")

    return b"".join(
                [
                    pack( "!H" , HARDWARE_TYPE),
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

def parse_arp_response(packet):
    eth_header = packet[0:14]
    arp_header = packet[14:42]

    eth = unpack("!6s6s2s", eth_header)
    arp = unpack("!2s2s1s1s2s6s4s6s4s", arp_header)

    src_mac = binascii.hexlify(arp[5]).decode()
    src_ip = socket.inet_ntoa(arp[6])
    print(f"DEBUG :: src_mac = {src_mac}")
    print(f"DEBUG :: src_ip = {src_ip}")

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
            _debug = False
        ) -> None:
        try :
            self.interface = interface or IP_Address(ip =src_ip).get_interface()
        except IP_Error:
            self.interface = IP_Address(socket.gethostbyname(socket.gethostname())).get_interface()

        self.op = operation or "REQ"  
        self.src_mac = src_mac or _local_mac()
        self.dest_mac = dest_mac
        """
            it will raise if it's error here
        """
        self.packet = _make_arp_packet(self.op , self.src_mac , src_ip , self.dest_mac , dest_ip)
        self.rec_packet = None
        self.debug = _debug
        if self.debug:
            debug(msg = "Debug Enable")
        self.connection()



    def connection(self):
        if self.debug:
            debug(msg = f"arp operation : {self.op}")
            debug(msg = f"packet : {self.packet}")

        with socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003)) as sock:
            sock.bind((self.interface, 0))

            if self.debug:
                debug(msg = f"bind on {self.interface} interface")

            
            eth_header = b"".join(
                    [
                        pack("!6s" , self.dest_mac),
                        pack("6s", self.src_mac),
                        pack("H",  0x0806)
                    ]
                )
            if self.debug:
                debug(msg = f"creating arp header {eth_header}")

            packet = eth_header + self.packet

            # Send packet
            sock.send(packet)
            if self.debug:
                debug(msg = f"sending packet : {packet}")

            # Listen for ARP reply
            while True:
                received_packet, addr = sock.recvfrom(65535)
                if self.debug:
                    debug(msg = f"reciving packet : {received_packet}")
                eth_type, = unpack("!H", received_packet[12:14])
                if eth_type == 0x0806:  # ARP packet
                    arp_opcode, = unpack("!H", received_packet[20:22])
                    parse_arp_response(received_packet)
                    if arp_opcode == 0x0002:  # ARP reply
                        #return (self.extract_header(received_packet))
                        #self.rec_packet = received_packet
                        parse_arp_response(received_packet)
                        break
        return True
    def check(self):
        return self.rec_packet is not None

    def get_packet(self):
        return self.rec_packet

#ARP(operation = "REQ" , dest_ip = "192.168.0.200").connection()
