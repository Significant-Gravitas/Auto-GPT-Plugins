#!/bin/bash

isort .
black --exclude='.*\/*(dist|venv|.venv|test-results)\/*.*' .