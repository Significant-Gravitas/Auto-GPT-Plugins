clean:
	@rm -rf build 2>/dev/null || true
	@rm -rf dist 2>/dev/null || true
	@rm -rf __pycache__ 2>/dev/null || true
	@rm -rf *.egg-info 2>/dev/null || true
	@rm -rf **/*.egg-info 2>/dev/null || true
	@rm -rf *.pyc 2>/dev/null || true
	@rm -rf **/*.pyc 2>/dev/null || true
	@rm -rf reports 2>/dev/null || true

qa:
	@flake8 .
	@python run_pylint.py

style:
	@isort .
	@black --exclude='.*\/*(dist|venv|.venv|test-results)\/*.*' .


.PHONY: clean qa style
