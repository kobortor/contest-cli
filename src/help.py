from typing import *

def handle_help(args: List[str]):
    if args:
        print("Please do not put arguments after help")

    print("config:\n{}\n".format(help_config()))
    print("make:\n{}\n".format(help_make()))
    print("submit:\n{}\n".format(help_submit()))

def help_config():
    return "CONFIG HELP TEXT"

def help_make():
    return "MAKE HELP TEXT"

def help_submit():
    return "SUBMIT HELP TEXT"
