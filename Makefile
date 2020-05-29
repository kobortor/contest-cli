python_files = src/__main__.py src/help.py src/config.py src/submit.py src/make.py src/utils.py
app: $(python_files)
	@tmp=$$(mktemp); \
	zip -j "$$tmp.zip" $(python_files); \
	echo '#!/usr/bin/env python3' | cat - "$$tmp.zip" > app; \
	chmod a+x app; \
	rm "$$tmp" "$$tmp.zip"
