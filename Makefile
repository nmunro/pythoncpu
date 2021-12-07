.PHONY: env run test lint requires docs compile
.DEFAULT: env

FILES = `find examples -type f -name '*.bin'`
BUILDS = `find examples -type f -name '*.out'`

env:
	@python -m venv .venv
	@poetry install

run:
	@poetry run python cpu/main.py --load $(LOAD)

test:
	@poetry run coverage run --branch -m unittest discover --pattern=tests/*.py && poetry run coverage html

requires:
	@poetry show --no-dev | tr -s " " | sed 's/ /==/' | sed 's/ .*//' > requirements.txt

lint:
	@poetry run isort --virtual-env .venv cpu/*.py && poetry run flake8

docs:
	@poetry run sphinx-apidoc -f -o docs/source/ cpu ./tests/*.py
	@cd docs && make html

compile:
	@poetry run python cpu/tools/compiler.py --input $(INPUT) --output $(OUTPUT)

compile-all:
	@for file in $(FILES); do make compile INPUT=$$file OUTPUT=$$file.out; done

clean:
	@for file in $(BUILDS); do rm $$file; done
