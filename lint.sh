#!/usr/bin/env bash

set -x

autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place app --exclude=__init__.py
isort --multi-line=3 --trailing-comma --force-grid-wrap=0 --combine-as --line-width 100 --recursive --apply app
black --line-length=100 app
