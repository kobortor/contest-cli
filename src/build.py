from typing import *
from utils import Settings
import os

def build_target(source_file, output_file, compile_fmt_str) -> bool:
    compile_command = compile_fmt_str
    compile_command = compile_command.replace("${SOURCE}", source_file)
    compile_command = compile_command.replace("${OUTPUT}", output_file)
    compile_command = compile_command.strip()

    if not compile_command:
        return False

    code = os.system(compile_command)
    if code != 0:
        return False

    return True

def handle_build(args: List[str]):
    """
    Returns True if build was successful, False otherwise
    """
    settings = Settings.get_saved()
    if not settings.language.is_compiled:
        print("You don't need to build {}".format(settings.language.name))
        return

    output_file = "a.out" if settings.language.outfile is not None else settings.language.outfile
    for i in range(len(args)):
        if args[i].startswith("-o"):
            if args[i] == "-o":
                if i == len(args) - 1:
                    print("Need something to follow '-o'")
                    return
                else:
                    output_file = args[i + 1]
                    args = args[:i] + args[i+2:]
                    break
            else:
                output_file = args[i][2:].strip()
                args = args[:i] + args[i+1:]

    source_file = ""
    if not args:
        if settings.working_file is None:
            print("No working file found!")
            return

        source_file = settings.working_file
    elif len(args) == 1:
        source_file = args[0]
    else:
        print("I don't know what to do with more than 1 parameter!")
        print("Did you mean to put '\\ ' instead of ' ' when entering your filenames?")
        return

    if build_target(source_file, output_file, compile_fmt_str):
        print("Build success!")
    else:
        print("Build failure!")
