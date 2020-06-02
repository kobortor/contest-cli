#!/usr/bin/env python3

import sys
from typing import *
from help import handle_help
from config import handle_config
from make import handle_make
from submit import handle_submit
from build import handle_build

def main():
    if len(sys.argv) == 1:
        print("Please choose an option: [config, make, submit, help]")
        sys.exit(1)
    
    first_arg = sys.argv[1]
    remaining_args = sys.argv[2:]

    if first_arg == "config":
        handle_config(remaining_args)
    elif first_arg == "make":
        handle_make(remaining_args)
    elif first_arg == "submit":
        handle_submit(remaining_args)
    elif first_arg == "help":
        handle_help(remaining_args)
    elif first_arg == "build":
        handle_build(remaining_args)
    else:
        print("Argument {} not understood".format(sys.argv[1]))

if __name__ == "__main__":
    main()
