.PHONY: init lint crawling run clean remove

NAME = Creation_LLM

SHELL := bash
python = python3

ifeq ($(OS),Windows_NT)
	python := python
endif

ifdef user
	pip_user_option = --user
endif

init:
	$(python) -m pip install $(pip_user_option) --upgrade pip
	$(python) -m pip install $(pip_user_option) -r requirements.txt
	pre-commit install

lint:
	$(python) -m isort --settings-file=.isort.cfg ./
	$(python) -m flake8 --config=.flake8 ./

crawling:
	$(python) crawler.py

run:
	streamlit run main.py

clear:
	rm -fr **/__pycache__/

remove:
	rm -fr **/chromedriver \
	rm -fr data/**.txt
