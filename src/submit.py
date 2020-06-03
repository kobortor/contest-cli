#!/usr/bin/env python3

from typing import *
from utils import Settings


def handle_submit(args: List[str]):
    if len(args) == 0:
        settings = Settings.get_saved()
    elif len(args) == 1:
        pass
    elif len(args) == 2:
        pass
    else:
        print("Cannot understand more than 2 arguments to `submit`")
