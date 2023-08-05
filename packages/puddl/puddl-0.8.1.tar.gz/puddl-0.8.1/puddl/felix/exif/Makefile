.PHONY: default
default: load generate

.PHONY: load
load:
	./load.py /tmp/pics

.PHONY: generate
generate:
	puddl db shell exif < definitions.sql
	./generate.py > data.js

.PHONY: show
show:
	firefox index.html
