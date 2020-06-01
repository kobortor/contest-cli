#!/bin/bash

sudo cp dmoj /usr/local/bin/
mkdir -p ~/.contest-cli/dmoj-defaults
cp $@ ~/.contest-cli/dmoj-defaults/
