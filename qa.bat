@call python -m flake8 . || exit \b 1
@call python run_pylint.py || exit \b 1
