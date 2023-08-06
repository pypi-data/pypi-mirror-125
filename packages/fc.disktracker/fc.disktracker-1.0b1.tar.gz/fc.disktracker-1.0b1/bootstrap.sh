#!/bin/sh
set -e
rm -rf bin lib include 
python3 -m venv .
bin/pip install -e '.[test]'
