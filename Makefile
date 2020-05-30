python_files = src/__main__.py src/help.py src/config.py src/submit.py src/make.py src/utils.py
default_files = defaults/patterns.json

dmoj: $(python_files)
	@tmp=$$(mktemp); \
	zip -j "$$tmp.zip" $(python_files); \
	echo '#!/usr/bin/env python3' | cat - "$$tmp.zip" > dmoj; \
	chmod a+x dmoj; \
	rm "$$tmp" "$$tmp.zip"

.PHONY: install
install: dmoj
	@cp dmoj /usr/local/bin/; \
	mkdir -p ~/.contest-cli/dmoj-defaults; \
	cp $(default_files) ~/.contest-cli/dmoj-defaults/

