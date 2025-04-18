#!/bin/bash

isort ./
flake8 ./
black --skip-string-normalization ./