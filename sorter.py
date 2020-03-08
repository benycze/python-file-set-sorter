#!/usr/bin/env python3

# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

import sys
import traceback

import sorter

def main():
    args = sorter.parse_arguments(sys.argv[1:])
    if args.strip < 0:
        print("Strip parameter cannot be a negative value!")
        sys.exit(1)

    # Convert all files into the structure with configuration files
    try:
        unique_file_list = [sorter.FileStream(f,args.strip,args.debug) for f in args.unique_files]
        other_file_list = [sorter.FileStream(f,args.strip,args.debug) for f in args.other_files]

        # Run the analysis
        alg = sorter.AnalyzeFiles(unique_file_list, other_file_list,args.debug)
        alg.analyze()
        alg.print_results()
    except Exception:
        print(traceback.format_exc())
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
