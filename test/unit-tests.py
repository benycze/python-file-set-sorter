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


class TestFileStream(unittest.TestCase):

    def __get_lines(self,file):
        """
        Get the contnet of the file

        Parameters:
            - file - file path

        Return the list of lines
        """
        f = open(file,'r')
        ret = f.readlines()
        f.close()
        return  [line.strip() for line in ret]


    def __check_fs_test(self,stripdef,stripexp,fileIn,fileRes,unmodlines,reslines):
        """
        Run the check of the filestream.

        Parameters:
            - stripdef - default strip value
            - stripexp - expected strip value
            - fileIn - input file path
            - fileRes - file path with results
            - unmodlines - lines with not modified input
            - reslines - stripped lines
        """
        # Run the test, load the file
        fs = sorter.analyze.FileStream(fileIn,stripdef,False) 
        
        # Check results
        self.assertEqual(fs.file,fileIn)
        self.assertEqual(fs.strip,stripexp)

        self.assertListEqual(fs.lines,unmodlines)
        self.assertEqual(fs.fset,set(reslines))


    def test_fs(self):

        fileIn  = "data/setA1.txt"
        fileRes = "data/setA1Res.txt"
        reslines = self.__get_lines(fileRes)
        unmodlines = self.__get_lines(fileIn)
        self.__check_fs_test(3,3,fileIn,fileRes,unmodlines,reslines)

        fileIn  = "data/setA1Strip.txt"
        fileRes = "data/setA1StripRes.txt"
        reslines = self.__get_lines(fileRes)
        unmodlines = self.__get_lines(fileIn)[1:]
        self.__check_fs_test(3,2,fileIn,fileRes,unmodlines,reslines)


class TestAnalyzer(unittest.TestCase):

    def test_analyzer(self):
        pass

if __name__ == "__main__":
    unittest.main()