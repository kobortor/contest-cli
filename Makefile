python_files = src/__main__.py src/help.py src/config.py src/submit.py src/make.py src/utils.py
default_files = defaults/patterns.json defaults/settings.json defaults/languages.json

dmoj: $(python_files)
	@tmp=$$(mktemp); \
	zip -j "$$tmp.zip" $(python_files); \
	echo '#!/usr/bin/env python3' | cat - "$$tmp.zip" > dmoj; \
	chmod a+x dmoj; \
	rm "$$tmp" "$$tmp.zip"

.PHONY: install
install: dmoj
	@bash scripts/install.sh $(default_files)

.PHONY: uninstall
uninstall:
	@bash scripts/uninstall.sh $(default_files)
