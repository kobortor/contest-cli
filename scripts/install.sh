#!/bin/bash

sudo cp dmoj /usr/local/bin/
mkdir -p "$HOME/.contest-cli/dmoj"

for f in {languages,patterns,settings}.json; do
    if [ -f "$HOME/.contest-cli/dmoj/$f" ]; then
        echo "File $f found, not overwriting... To overwrite, use 'make hard-install'"
    else
        cp "defaults/$f" "$HOME/.contest-cli/dmoj/$f"
    fi
done
