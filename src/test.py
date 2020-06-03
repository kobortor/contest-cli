#!/usr/bin/env python3

import os
from typing import *
from utils import Settings


def handle_test(args: List[str]):
    settings = Settings.get_saved()
    if not settings.has_problem():
        print("You don't seem to have a problem set")
        return

    # TODO
