#!/usr/bin/env python3
import json
import os
from typing import *
from typing import BinaryIO

from utils import Settings
import subprocess
import status_code

def handle_test(args: List[str]):
    settings = Settings.get_saved()
    if not settings.has_problem():
        print("You don't seem to have a problem set")
        return

    problem_attrs_filename = os.path.join(
        settings.sample_data_folder,
        settings.sample_problem_attribute_filename)
    if not os.path.isfile(problem_attrs_filename):
        print("There doesn't seem to be a problem attributes file. Did you change a setting?")
        return

    problem_attrs = json.load(open(problem_attrs_filename, "r"))

    samples = problem_attrs.get("samples", [])
    for sample in samples:
        sample_in_filename = os.path.join(
            settings.sample_data_folder,
            sample + ".in"
        )
        sample_out_filename = os.path.join(
            settings.sample_data_folder,
            sample + ".out"
        )

        if not os.path.isfile(sample_in_filename):
            print("Sample {} doesn't have an input file... Skipping")
            continue

        if not os.path.isfile(sample_out_filename):
            print("Sample {} doesn't have an input file... Skipping")
            continue

        user_out_filename = os.path.join(
            settings.sample_data_folder,
            sample + ".tmp"
        )

        user_out_file = open(user_out_filename, "rb")

        if settings.language.is_compiled:
            proc = subprocess.Popen(
                settings.language.run_fmt_str.replace("${OUTPUT}", settings.language.outfile),
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE)

            # hopefully you don't have gigabytes of data
            proc.stdin.write(open(sample_in_filename, "rb").read())
            proc.stdin.flush()

            total_output_len = 0

            while True:
                return_code = proc.poll()
                if return_code is not None:
                    # TODO Handle codes
                    print("Returned with code {}".format(return_code))
                    break
                else:
                    new_output = proc.stdout.readline()
                    total_output_len += new_output
                    if total_output_len + total_output_len > 1024 * 1024:
                        print(status_code.COLORED_OLE)
                        break

                    user_out_file.write(new_output)
        else:
            print("We don't support non-compiled stuff yet")

        user_out_file.close()
        # Diff user_out_file and the answer output file
