.PHONY: all docs init clean

all:
	python tennis/main.py

docs:
	PYTHONPATH=./tennis pdoc -o ./docs tennis -d google

docs-live:
	PYTHONPATH=./tennis pdoc --host localhost tennis -d google

init:
	pip requirements.txt

clean:
	rm -rf docs
