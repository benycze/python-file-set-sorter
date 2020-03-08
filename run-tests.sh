#!/usr/bin/env bash

# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

export PYTHONPATH=`pwd`${PYTHONPATH:+:${PYTHONPATH}}
python3 test/unit-tests.py
