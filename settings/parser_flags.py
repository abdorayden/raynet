"""
    parser_flags file is part of raynet tool
"""

from settings.config import *

import argparse
import sys

class Arg_Parse_With_Err(argparse.ArgumentParser):
    def error(self,message):
        self.print_usage(sys.stderr)
        err_message = error(msg = message ,ret = True)
        self.exit(2 , err_message)
    def format_usage(self):
        custom_usage = info(msg = f"{sys.argv[0]} [IP/DOMAIN/TARGET] [ARGUMENTS]\n" , ret = True)
        return custom_usage

def flags() -> None :
    flag = Arg_Parse_With_Err(
    epilog=
    f"""
        EXAMPLE :
           {sys.argv[0]} 10.10.10.10 --osi network --protocole arp --scan --verbose
    """
    )
    flag.add_argument(
            "target" , 
            help = "Target IP Address or domain name"
    )
    Group1 = flag.add_argument_group(info("Groupe1", ret = True) ,"Informations and Default Flags" )
    Group1.add_argument(
            "-p" , 
            "--port" , 
            type = str ,
            metavar = 'N' , 
            help = "Target Port"
    )
    Group1.add_argument(
            "-o" , 
            "--out" , 
            default = "raynet.out",
            help = "out file path"
    )
    Group1.add_argument(
            "-I",
            "--interface" , 
            default = None ,
            help = "interface to work with"
    )
    Group1.add_argument(
            "-v",
            "--verbose" , 
            action='store_true', 
            help = "enable verbose mode"
    )
    Group1.add_argument(
            "-V",
            "--version",
            action='version', 
            version=f'{sys.argv[0]} : {version}',
            help = "show version"
    )
    Group1.add_argument(
            "-d",
            "--debug" , 
            action = "store_true",
            help = "enable debug"
    )
    Group1.add_argument(
            "--no-banner" , 
            action = "store_true",
            help = "display banner OFF"
    )
    Groupe2 = flag.add_argument_group(info("Groupe2", ret = True) ,"Scanning and Enumeration" )
    Groupe2.add_argument(
            "-s" , 
            "--scan" , 
            action = "store_true",
            help = "enable scaning"
    ) 
    Groupe2.add_argument(
            "-O" , 
            "--osi" , 
            default = "transport.tcp",
            help = "work with osi model"
    ) 
    Groupe2.add_argument(
            "-P" , 
            "--protocole" , 
            help = "work with protocole"
    ) 
    Groupe2.add_argument(
            "-E" , 
            "--enum" , 
            help = "start enumeration"
    )
    Groupe2.add_argument(
            "-os" , 
            "--op-system" , 
            help = "operating system enumeration"
    )
    Groupe3 = flag.add_argument_group(info("Groupe3", ret = True) ,"Modules and External Scripts" )
    Groupe3.add_argument(
        "-M",
        "--module",
        help = "use module"
    )
    Groupe3.add_argument(
        "--module-info",
        help = "Display module information"
    )
    Groupe3.add_argument(
        "--module-list",
        help = "list modules"
    )
    Groupe3.add_argument(
        "--module-args",
        help = "add module arguments"
    )
    # TODO: add flags for vulnerability scaning and Exploits 
    return flag.parse_args()

