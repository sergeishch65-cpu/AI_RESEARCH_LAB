.PHONY: install doctor demo test lint notebook-check verify clean-generated challenge-doctor challenge-sources challenge-trackio-smoke challenge-test challenge-audit

VENV_PYTHON := .venv/bin/python
JUPYTER_EXEC := .venv/bin/jupyter

install:
	python3 -m venv .venv
	.venv/bin/pip install --upgrade pip setuptools wheel
	.venv/bin/pip install -r requirements.txt -e .

doctor:
	$(VENV_PYTHON) -m ai_research_lab.cli doctor

demo:
	$(VENV_PYTHON) -m ai_research_lab.cli run demo_study

test:
	$(VENV_PYTHON) -m pytest

lint:
	$(VENV_PYTHON) -m ruff check src tests

notebook-check:
	$(JUPYTER_EXEC) nbconvert --to notebook --execute notebooks/00_lab_smoke_test.ipynb --output /tmp/00_lab_smoke_test.executed.ipynb --ExecutePreprocessor.timeout=120 --ExecutePreprocessor.kernel_name=python3

verify:
	$(VENV_PYTHON) -m ai_research_lab.cli verify demo_study

challenge-doctor:
	$(VENV_PYTHON) -m ai_research_lab.cli challenge doctor

challenge-sources:
	$(VENV_PYTHON) -m ai_research_lab.cli challenge sources-sync

challenge-trackio-smoke:
	$(VENV_PYTHON) -m ai_research_lab.cli challenge trackio-smoke

challenge-test:
	$(VENV_PYTHON) -m pytest -q

challenge-audit:
	$(VENV_PYTHON) -m pip check && $(VENV_PYTHON) -m ruff check src tests && $(VENV_PYTHON) -m pytest -q && $(VENV_PYTHON) -m ai_research_lab.cli challenge doctor

clean-generated:
	rm -rf research/demo_study/experiments/*
	rm -rf research/demo_study/results/*
	rm -rf research/demo_study/figures/*
	rm -rf research/demo_study/logs/*
	rm -rf research/demo_study/logbook/*
