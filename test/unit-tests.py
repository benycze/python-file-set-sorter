#!/usr/bin/env python3

# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

import unittest
import pdb

import sorter.analyze
import sorter.arguments


class TestArgParser(unittest.TestCase):
    """
    Unit test for the argument parsing from the command line
    """

    
    def test_parsing(self):
        argv =  ["unit-tests.py","--strip","4","--unique-files","fileA","fileB:4","--other-files","fileC:2","fileD"]
        unique_list  = ["fileA","fileB:4"]
        other_list = ["fileC:2","fileD"]

        args=sorter.arguments.parse_arguments(argv)
        self.assertEqual(args.debug,False) 
        self.assertEqual(args.strip,4) 
        self.assertListEqual(args.unique_files,unique_list)
        self.assertListEqual(args.other_files,other_list)      


    def test_no_strip(self):
        argv =  ["unit-tests.py","--unique-files","fileA","--other-files","fileD"]
        unique_list  = ["fileA"]
        other_list = ["fileD"]

        args=sorter.arguments.parse_arguments(argv)
        self.assertEqual(args.debug,False) 
        self.assertEqual(args.strip,0) 
        self.assertListEqual(args.unique_files,unique_list)
        self.assertListEqual(args.other_files,other_list)  

    def test_en_debug(self):
        argv =  ["unit-tests.py","--unique-files","fileA","--other-files","fileD","--debug"]
        unique_list  = ["fileA"]
        other_list = ["fileD"]

        args=sorter.arguments.parse_arguments(argv)
        self.assertEqual(args.debug,True) 
        self.assertEqual(args.strip,0) 
        self.assertListEqual(args.unique_files,unique_list)
        self.assertListEqual(args.other_files,other_list)         



if __name__ == "__main__":
    unittest.main()