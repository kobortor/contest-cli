#!/bin/bash

sudo cp dmoj /usr/local/bin/
mkdir -p ~/.contest-cli/dmoj

for f in defaults/{languages,patterns,settings}.json; do
    if [ -f "$f" ]; then
        echo "File $f found, not overwriting... To overwrite, use 'make hard-install'"
    fi
done
