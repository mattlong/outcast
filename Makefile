.PHONY: test


init:
	pip install -r requirements.txt

test:
	nosetests -sv --rednose
