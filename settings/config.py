"""
    config.py is part of the rayden tool
"""
Reset  = "\033[0m"
Black  = "\033[30m"
Red    = "\033[31m"
Green  = "\033[32m"
Yellow = "\033[33m"
Blue   = "\033[34m"
Purple = "\033[35m"
Cyan   = "\033[36m"
White  = "\033[37m"

version = "0.0.1"

Banner = f"""
\t\t\t\t   {Green}                    \       /
\t\t\t\t    {Green}                    \     /
\t\t\t\t     {Green}                    \   /
\t\t\t\t       {Green}                   \ /
\t\t\t\t                   {Green}- - - -{Red} O{Green} - - - -{Reset}
\t\t\t\t                           |
\t\t\t\t╦════╗╔════╦╦     ╦  ╔═══════════╗   ╦══╗  ╦╔════╗╔══╦══╗ 
\t\t\t\t║    ║║    ║║     ║  ║   {Red}o  {Yellow}o {Blue} o{Reset} ║   ║  ║  ║║        ║    
\t\t\t\t║    ║║    ║║     ║  ╠═══════════╣   ║  ║  ║║        ║    
\t\t\t\t╠══╦═╝╠════╣╚══╦══╝  ║   {Red}o  {Yellow}o {Blue} o{Reset} ║   ║  ║  ║╠════╣   ║    
\t\t\t\t║  ║  ║    ║   ║     ╠═══════════╣   ║  ║  ║║        ║    
\t\t\t\t║  ║  ║    ║   ║     ║ v : {Yellow}{version}{Reset} ║   ║  ║  ║║        ║    
\t\t\t\t╩  ╚ ═╩    ╩   ╩     ╚═══════════╝   ╩  ╩══╩╩════╝   ╩    

"""                          

def add_color(msg , color : str):
    return color + msg + Reset

def success(type = None , msg : str = "" , ret = False):
    if ret :
        return f"{add_color(type or '[SUCCESS]' , Green)} : {msg}\n"
    else :
        print(f"{add_color(type or '[SUCCESS]' , Green)} : {msg}")

def info(type = None , msg : str = "" , ret = False):
    if ret :
        return f"{add_color(type or '[INFO]' , Cyan)} : {msg}\n"
    else :
        print(f"{add_color(type or '[INFO]' , Cyan)} : {msg}")

def error(type = None , msg : str = "", ret = False):
    if ret :
        return f"{add_color(type or '[ERROR]' , Red)} : {msg}\n"
    else :
        print(f"{add_color(type or '[ERROR]' , Red)} : {msg}")

def warning(type = None , msg : str = "" , ret = False):
    if ret :
        return f"{add_color(type or '[WARNING]' , Yellow)} : {msg}\n"
    else:
        print(f"{add_color(type or '[WARNING]' , Yellow)} : {msg}")

def debug(type = None , msg : str = "" , ret = False):
    if ret :
        return f"{add_color(type or '[DEBUG]' , Blue)} : {msg}\n"
    else :
        print(f"{add_color(type or '[DEBUG]' , Blue)} : {msg}")

extentions = [
       "html",
       "json",
       "txt"
]

osi_map = {
        "network" : [
                "arp",
                "ip4",
                "ip6",
                "icmp",
                "igmp",
                "dhcp"
            ],
        "transport" : [
                "tcp",
                "udp",
                "dccp"
            ],
        "presentation" : [
                "xml",
                "tls",
                "tlv",
                "xdr",
                "html"
            ],
        "application" : [
                
            "AMQP",
            "BGP",
            "DHCP",
            "DNS",
            "FTP",
            "FTPS",
            "FXP",
            "Gemini",
            "Gopher",
            "H.323",
            "HTTP",
            "HTTPS",
            "IMAP",
            "IPP",
            "IRC",
            "LDAP",
            "LMTP",
            "MODBUS",
            "MQTT",
            "MYSQL",
            "NFS",
            "NNTP",
            "POP",
            "RDP",
            "REDIS",
            "RTSP",
            "SFTP",
            "SILC",
            "SIMPLE",
            "SIP",
            "SMB-CIFS",
            "SMTP",
            "SNMP",
            "SOAP",
            "SSH",
            "TCAP",
            "TFTP",
            "Telnet",
            "VoIP",
            "WebDAV",
            "XMPP"
            ]
}
