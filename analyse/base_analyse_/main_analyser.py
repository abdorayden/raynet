
# ARP
    #def extract_header(self,packet):
    #    eth_header = struct.unpack('!6s6sH', packet[:14])
    #    src_mac = binascii.hexlify(eth_header[0]).decode('utf-8')
    #    dst_mac = binascii.hexlify(eth_header[1]).decode('utf-8')
    #    ethertype = eth_header[2]

    #    arp_packet = struct.unpack('2s2s1s1s2s6s4s6s4s', packet[14:42])
    #    arp_opcode = int.from_bytes(arp_packet[4], byteorder='big')

    #    if arp_opcode == 1:
    #        src_ip = socket.inet_ntoa(arp_packet[6])
    #        src_mac = binascii.hexlify(arp_packet[5]).decode('utf-8')
    #        try:
    #            device_name = socket.gethostbyaddr(src_ip)[0]
    #        except socket.herror:
    #            device_name = "Unknown"

    #    return dst_mac, src_ip , device_name
