TEST_PATH=./

install:
	pip install -r requirements

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

test:clean
	py.test --verbose --color=yes -s $(TEST_PATH)
	coverage report

shell:clean
	ipython
