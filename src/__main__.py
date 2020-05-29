#!/usr/bin/env python3

import sys
from typing import *
import requests

def handle_config(args: List[str]):
    if not args:
        print("Config usage:")
    pass

def handle_make(args: List[str]):
    pass

def handle_submit(args: List[str]):
    pass

def main():
    print(sys.argv)
    if len(sys.argv) == 0:
        print("Please choose an option: [config, make, submit, help]")
        sys.exit(1)
    
    first_arg = sys.argv[0]
    if first_arg == "config":
        handle_config(sys.argv[1:])
    elif first_arg == "make":
        handle_make(sys.argv[1:])
    elif first_arg == "submit":
        handle_submit(sys.argv[1:])
    elif first_arg == "help":
        handle_help(sys.argv[1:])

if __name__ == "__main__":
    main()
