all: test format lint type_check

test:
	uv run --isolated --python=3.12 pytest -m "not (slow or gui)"
	uv run --isolated --python=3.13 pytest -m "not (slow or gui)"
	uv run --isolated --python=3.14 pytest -m "not (slow or gui)"

test_quick:
	uv run --isolated --python=3.12 pytest

install: update

install_editable: install
	uv pip install --editable .

update:
	uv sync --upgrade

upgrade: update

build:
	uv build

publish:
	uv build
	uv publish

format:
	uv run ruff check --select I --fix .
	uv run ruff format

lint:
	uv run ruff check

type_check:
	uv run mypy typings userdetect.py tests

.PHONY: test install install_editable update upgrade build publish format docs lint pin_docs_requirements
