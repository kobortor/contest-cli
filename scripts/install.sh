#!/bin/bash

sudo cp dmoj /usr/local/bin/
mkdir -p ~/.contest-cli/dmoj

for f in {languages,patterns,settings}.json; do
    if [ -f "~/.contest-cli/dmoj/$f" ]; then
        echo "File $f found, not overwriting... To overwrite, use 'make hard-install'"
    else
        cp "defaults/$f" "~/.contest-cli/dmoj/$f"
    fi
done
