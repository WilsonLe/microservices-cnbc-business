#! /bin/sh

venv/bin/autopep8 --in-place --recursive src 

venv/bin/isort src