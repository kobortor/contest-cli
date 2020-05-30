from typing import *
from utils import get_settings

def handle_submit(args: List[str]):
    if len(args) == 0:
        settings = get_settings()
    elif len(args) == 1:
        pass
    elif len(args) == 2:
        pass
    else:
        print("Cannot understand more than 2 arguments to `submit`")
