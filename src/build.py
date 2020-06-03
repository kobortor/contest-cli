from typing import *
from utils import Settings
import os


def build_target(source_file, output_file, compile_fmt_str) -> bool:
    compile_command = compile_fmt_str
    compile_command = compile_command.replace("${SOURCE}", source_file)
    compile_command = compile_command.strip()

    if not compile_command:
        return False

    code = os.system(compile_command)
    if code != 0:
        return False

    return True


def handle_build(args: List[str], lazy=True, quiet=False):
    if args:
        if not quiet:
            print("Please not put any arguments for handle_build")
        
        return False

    settings = Settings.get_saved()
    
