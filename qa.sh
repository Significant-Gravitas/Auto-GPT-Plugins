#!/bin/bash
set -euf -o pipefail
flake8 .
python run_pylint.py