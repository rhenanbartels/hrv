install:
	pip install -r requirements

clean:
	find . -name "*.pyc" -exec rm -rf {} \;

tests:clean
	nosetests
