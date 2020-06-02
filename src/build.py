from typing import *
from utils import Settings

def handle_build(args: List[str]):
    settings = Settings.get_saved()
    if not settings.language.is_compiled:
        return

    output_name = "a.out" if settings.language.outfile is not None else settings.language.outfile
    for i in range(len(args)):
        if args[i].startswith("-o"):
            if args[i] == "-o":
                if i == len(args) - 1:
                    print("Need something to follow '-o'")
                    return
                else:
                    output_name = args[i + 1]
                    args = args[:i] + args[i+2:]
                    break
            else:
                output_name = args[i][2:].strip()
                args = args[:i] + args[i+1:]

    filename = ""
    if not args:
        if settings.working_file is None:
            print("No working file found!")
            return

        filename = settings.working_file
    elif len(args) == 1:
        filename = args[0]
    else:
        print("I don't know what to do with more than 1 parameter!")
        print("Did you mean to put '\\ ' instead of ' ' when entering your filenames?")
        return

    compile_command = settings.language.compile_fmt_str.replace("${SOURCE}", "'{}'".format(filename)).strip()
    if not compile_command:
        # This might be a language that doesn't need to be compiled
        return
