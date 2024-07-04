import socket
import sys
from struct import pack
import subprocess
import os

try:
    from osi.network.ip4.exception import (
            Invalid_IP_Address,
            Address_Block_Unkonw,
            )
except ModuleNotFoundError :

    class IP_Error(Exception):
        pass
    
    class Invalid_IP_Address(IP_Error):
        pass
    
    class Address_Block_Unkonw(Invalid_IP_Address):
        pass

def _make_ip_packet(
        ip_proto : int = None,
        src_ip : str =  None,
        dest_ip : str = None,
        ttl : int = None
        ) -> bytes:

    ipv = 4
    ip_h_len = 5
    ip_t_len = 20
    """
        our OS will handle value of checksum
    """
    checksum = 0

    if ip_proto is None and src_ip is None and dest_ip is None :
        raise IP_Error("missing information in packet")
    if ttl is None :
        ttl = 255

    return b"".join(
                [
                    pack("!B",(ipv << 4) + ip_h_len),
                    pack("!B",0),  # Type of Service (socket will handle this)
                    pack("!H",ip_t_len),
                    pack("!H",0),  # Identification(socket will handle this)
                    pack("!H",0),  # Flags + Fragment Offset(socket will handle this)
                    pack("!B",ttl),
                    pack("!B",ip_proto),
                    pack("!H",checksum),
                    pack("!4s",socket.inet_aton(src_ip)),
                    pack("!4s",socket.inet_aton(dest_ip))
                ]
            )

class IP_Address(object):
    def __init__(self , ip: str):
        if ip is not None :
            self.ip = ip
        else:
            raise IP_Error("ip is None")
        self.interfaces = []
        self.is_range = "/" in ip
        self.iface = self.get_interface()
        self.address_block = [
                    24,
                    16,
                    8
                ]
        if not self.check_ip() :
            raise Invalid_IP_Address("out of range")

    def get_block(self):
        if "/" in self.ip :
            return int(self.ip.split("/")[1])
        else: 
            return False
    
    def check_ip(self):
        if self.is_range:
            return len(self.ip.split(".")) == 4 and all([int(x) >= 0 and int(x) <= 255 for x in self.ip.split("/")[0].split(".") ])
        else :
            return len(self.ip.split(".")) == 4 and all([int(x) >= 0 and int(x) <= 255 for x in self.ip.split(".")])

    def _generate_ips(self):
        ips : list[str] = []
        if self.is_range :
            if x := self.get_block() and x in self.address_block :
                if x == self.address_block[0]:
                    temp = self.ip.split("/")[0].split(".")
                    temp.pop(3)
                    for i in range(0,256):
                        ips.append(".".join(temp) + f".{i}")
                    return ips
                elif x == self.address_block[1] :
                    temp = self.ip.split("/")[0].split(".")
                    temp.pop(3)
                    temp.pop(2)
                    for i in range(0,256):
                        for j in range(0,256):
                            ips.append(".".join(temp) + f".{i}" + f".{j}")
                    return ips
                elif x == self.address_block[2] :
                    temp = self.ip.split("/")[0].split(".")
                    temp.pop(3)
                    temp.pop(2)
                    temp.pop(1)
                    for i in range(0,256):
                        for j in range(0,256):
                            for k in range(0,256):
                                ips.append(".".join(temp) + f".{i}" + f".{j}" + f"{k}")
                    return ips
            else :
                raise Address_Block_Unkonw("address block not in list [24,16,8]")
        else :
            return ips
    def get_interface(self):
        content = str(subprocess.run("ifconfig", capture_output = True)).removesuffix("', stderr=b'')").removeprefix("CompletedProcess(args='ifconfig', returncode=0, stdout=b'").split("\\n")
        ifaces = []
        for i in range(len(content)):
            if not content[i].startswith(" ") and ":" in content[i]:
                ifaces.append((content[i].split(":")[0] , i))
                self.interfaces.append(content[i].split(":")[0])
            else:
                if("inet" in content[i]):
                    for j in content[i].split("inet"):
                        if ".".join(self.ip.split(".")[:-2]) in j :
                            for k in range(len(ifaces),0,-1) :
                                if i > ifaces[k - 1][1]:
                                    return (ifaces[k - 1][0])


