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

def success(msg : str):
    print(f"{add_color('[SUCCESS]' , Green)} : {msg}")

def info(msg : str):
    print(f"{add_color('[INFO]' , Cyan)} : {msg}")

def error(msg : str):
    print(f"{add_color('[ERROR]' , Red)} : {msg}")

def warning(msg : str):
    print(f"{add_color('[WARNING]' , Yellow)} : {msg}")

def debug(msg : str):
    print(f"{add_color('[DEBUG]' , Blue)} : {msg}")

extentions = [
       "html",
       "json",
       "txt",
       "toml"
]
