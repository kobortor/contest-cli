python_files = src/__main__.py src/help.py src/config.py src/submit.py src/make.py src/utils.py src/build.py src/test.py

dmoj: $(python_files)
	@tmp=$$(mktemp); \
	zip -j "$$tmp.zip" $(python_files); \
	echo '#!/usr/bin/env python3' | cat - "$$tmp.zip" > dmoj; \
	chmod a+x dmoj; \
	rm "$$tmp" "$$tmp.zip"

# Install everything, do not overwrite data
.PHONY: install
install: dmoj
	@bash scripts/install.sh

# Install everything, overwrite userdata
.PHONY: hard-install
hard-install: dmoj
	@bash scripts/hard-install.sh

# Deletes just the program
.PHONY: uninstall
uninstall:
	@bash scripts/uninstall.sh

# Deletes the user data too
.PHONY: hard-uninstall
hard-uninstall:
	@bash scripts/hard-uninstall.sh
