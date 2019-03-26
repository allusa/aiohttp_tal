.PHONY: test
test:
	pytest --flake8 --cov=aiohttp_tal

.PHONY: testcov
testcov:
	pytest --flake8 --cov=aiohttp_tal --cov-report=html
	@echo "open file://`pwd`/htmlcov/index.html"

.PHONY: doc
doc:
	make -C docs html
	@echo "open file://`pwd`/docs/_build/html/index.html"
