#!/usr/bin/env bash

export PYTHONPATH=src:tests
python3 -m unittest discover
