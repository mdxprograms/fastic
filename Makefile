.Phony: dev build create-venv install


dev:
	@. ./venv/bin/activate; python3 fastic.py;

build:
	@. ./venv/bin/activate; python3 fastic.py build;

create-venv:
	@python3 -m venv venv; . ./venv/bin/activate; pip install -r requirements.txt;

install:
	@. ./venv/bin/activate; pip install -r requirements.txt;
