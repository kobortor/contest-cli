from typing import *
from utils import Settings
import subprocess
import os


def build_target(source_file: str, compile_fmt_str: str, quiet: bool = False) -> bool:
    compile_command = compile_fmt_str
    compile_command = compile_command.replace("${SOURCE}", source_file)
    compile_command = compile_command.strip()

    if not compile_command:
        return False

    code = subprocess.call(compile_command)
    if code != 0:
        return False

    return True


def handle_build(args: List[str], lazy: bool = True, quiet: bool = False) -> None:
    if args:
        if not quiet:
            print("Please not put any arguments for handle_build")
        
        return

    settings = Settings.get_saved()
    if not settings.has_problem():
        print("You don't seem to have a problem loaded")
        return

    if lazy:
        modif_time = str(os.stat(settings.working_file).st_mtime_ns)
        if str(modif_time) == settings.last_build_time:
            print("No change since last update. Not building.")
            return

    if build_target(settings.working_file, settings.language.compile_fmt_str):
        if not quiet:
            print("Compilation Success")
    else:
        if not quiet:
            print("Compilation Failed")
