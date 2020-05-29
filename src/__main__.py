#!/usr/bin/env python3

import sys
from typing import *
from help import handle_help
from config import handle_config
from make import handle_make
from submit import handle_submit

def main():
    if len(sys.argv) == 1:
        print("Please choose an option: [config, make, submit, help]")
        sys.exit(1)
    
    first_arg = sys.argv[1]
    if first_arg == "config":
        handle_config(sys.argv[2:])
    elif first_arg == "make":
        handle_make(sys.argv[2:])
    elif first_arg == "submit":
        handle_submit(sys.argv[2:])
    elif first_arg == "help":
        handle_help(sys.argv[2:])
    else:
        print("Argument {} not understood".format(sys.argv[1]))

if __name__ == "__main__":
    main()
