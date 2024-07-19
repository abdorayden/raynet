#!/usr/bin/env python3

class ARPError(Exception):
    pass

class ConnectionTimeout(ARPError):
    pass
