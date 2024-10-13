init:
	pip install -r requirements.txt

test:
	nosetests tests

run:
	python main.py