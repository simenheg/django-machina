staticfiles:
	npm run gulp

messages:
	cd machina && django-admin.py makemessages -a

compiledmessages:
	cd machina && django-admin.py compilemessages

.PHONY: install upgrade lint coverage travis docs

install:
	pip install -r requirements-dev.txt
	pip install -e .

upgrade:
	pip install -r requirements-dev.txt -U
	pip install -e . -U

lint:
	flake8

coverage:
	py.test --cov-report term-missing --cov machina

spec:
	py.test --spec -p no:sugar

travis: install lint coverage

docs:
	cd docs && rm -rf _build && make html
