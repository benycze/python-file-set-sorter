
#!/usr/bin/env python3

# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

__all__ = ["analyze","arguments"]

# Export just the portion of the package
from .analyze import AnalyzeFiles, FileStream
from .arguments import parse_arguments
