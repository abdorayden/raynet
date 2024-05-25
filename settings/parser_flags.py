"""
    parser_flags file is part of raynet tool
"""

import sys

from settings.config import info

all_flags = [
        sys.argv[0],
        "-h",
        "--help",
        "-I",
        "--ip-addr",
        "-p",
        "--port",
        "-o",
        "--out",
        "--interface",
        "--verbose",
        "-v",
        "-d",
        "--debug",
        "--no-banner",
        "--module",
        "-M",
        "--module-info",
        "--module-args",
        "--scan",
        "--scan-default",
        "-S",
        "--osi",
        "-O",
        "--protocole",
        "-P",
        "--enumerate",
        "-E",
        "--op-system",
        "-os",
]

__all__ = [
            "ParserError",
            "Parser",
        ]

class ParserError(Exception):
    pass

class Parser(object):
    def __init__(self, description: str = "", banner: str = "", my_own_help_msg: str = None) -> None:
        self.args: list[str] = sys.argv
        self.my_args: list[str] = []
        self.banner = banner
        self.my_help_message = my_own_help_msg
        self.description = description
        self.values = {}
    def add_argument(self, *args_: tuple, help_: str = "", need_value: bool = False) -> None:
        self.my_args.append(tuple(args_) + (help_,))
        def decf(fn):
            def wrapper(*ar, **kw):
                if any(val in self.args for val in args_ if len(args_) > 1):
                    if need_value:
                        try :
                            if self.args[args_.index(args_[0]) + 2].startswith("-") :
                                raise ParserError
                            self.values.update((_arg , self.args[args_.index(args_[0]) + 2]) for _arg in list(args_))
                            fn( self.values[list(args_)[0]], *ar, **kw)
                        except IndexError :
                            raise ParserError(f"missing value for the \'{' or '.join(args_)}\' flags")
                    else :
                        fn(*ar, **kw)
            return wrapper
        return decf

    def help_message(self) -> None:
        before_message: str = f"usage : {self.args[0]} [ARGUMENTS]"
        print(self.banner)
        info(self.description)
        info(before_message + "\n")
        for *_arg, _help in self.my_args:
            print(" , ".join(_arg), end="\t\t")
            print(_help)
