.PHONY: all docs init clean

all:
	python tennis/main.py

docs:
	pdoc -o ./docs tennis

init:
	pip requirements.txt

clean:
	rm -rf docs
