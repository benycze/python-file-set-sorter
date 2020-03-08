#!/usr/bin/env python3

# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

import argparse
import sys
import analyze
import traceback

def parse_arguments():
    """
    Parse input arguments passed from the command line

    Return: The function return the dictionary with parsed arguments
    """
    parser = argparse.ArgumentParser(description='Process two sets of files and search for a unique files in the start group. '
        'The program tries to find a unique files in Set A that are not in the Set B. '
        'The format of input data is a text file where each file is on a line ending with a \\n character. Empty lines are filtered out.\n\n'
        'The format of unique files can contain the strip value which removes the first n paths from each analyzed files. The value can be defined '
        'globally or localy per file in the form FILE:STRIP, where the file is a file path and STRIP is the strip value.'
        'The default value (passed via the --strip argumnet) is assined iff the STRIP value is not defined.\n\n'
        'Another possibility is to define a strip value directly in a file as the first line of the file where the format is STRIP=value, where '
        'the value is a positive integer. The value inside the file has a bigger priority than value passed by in the argument.')

    # Add arguments
    parser.add_argument('--unique-files',type=str,nargs='+',help='The set of files which will be analyzed in the unique set (= Set A)',required=True)
    parser.add_argument('--other-files',type=str,nargs='+',help='The set of files which will be analyzed in the non-unique set (= Set B) ',required=True)
    parser.add_argument('--strip',type=int,help='Default strip value for all passed files. The default value is 0.',default=0)
    parser.add_argument('--debug',action='store_true',help="Enable the debug mode for the analysis.")

    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.strip < 0:
        print("Strip parameter cannot be a negative value!")
        sys.exit(1)

    # Convert all files into the structure with configuration files
    try:
        unique_file_list = [analyze.FileStream(f,args.strip,args.debug) for f in args.unique_files]
        other_file_list = [analyze.FileStream(f,args.strip,args.debug) for f in args.other_files]

        # Run the analysis
        alg = analyze.AnalyzeFiles(unique_file_list, other_file_list,args.debug)
        alg.analyze()
        alg.print_results()
    except Exception:
        print(traceback.format_exc())
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()
