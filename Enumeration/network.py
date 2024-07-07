"""
    Network Model Enumeration
"""
import struct

from Enumeration import Base_Analyse

class Enum_ARPacket(Base_Analyse):
    def __init__(self , packet) -> None : 
        super().__init__()
        self.packet = packet

        self.device_name = None
        self.src_ip = None
        self.dst_mac = None
        self.extract_header()

    def get_dst_mac(self):
        return self.dst_mac

    def get_src_ip(self):
        return self.src_ip

    def get_device_name(self):
        return self.device_name

    def extract_header(self):
        eth_header = struct.unpack('!6s6sH', self.packet[:14])
        src_mac = binascii.hexlify(eth_header[0]).decode('utf-8')
        self.dst_mac = binascii.hexlify(eth_header[1]).decode('utf-8')
        ethertype = eth_header[2]

        arp_packet = struct.unpack('2s2s1s1s2s6s4s6s4s', self.packet[14:42])
        arp_opcode = int.from_bytes(arp_packet[4], byteorder='big')

        if arp_opcode == 1:
            self.src_ip = socket.inet_ntoa(arp_packet[6])
            src_mac = binascii.hexlify(arp_packet[5]).decode('utf-8')
            try:
                self.device_name = socket.gethostbyaddr(src_ip)[0]
            except socket.herror:
                self.device_name = "Unknown"

        #return dst_mac, src_ip , device_name
