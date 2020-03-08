#!/usr/bin/env bash

# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

set -e

export PYTHONPATH=`pwd`${PYTHONPATH:+:${PYTHONPATH}}
cd test
python3 unit-tests.py

echo "We are done ..."
exit 0
