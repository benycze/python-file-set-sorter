#!/usr/bin/env python3

# Copyright 2020 by the project contributors
# SPDX-License-Identifier: GPL-3.0-only
#
# Author(s): Pavel Benacek <pavel.benacek@gmail.com>

import os

def strip_line(line,strip):
    """
    Take a line and perform a strip operation

    Parameter:
        - line - line to analyze
        - strip - strip value
    """
    # We want to skip the first element (absolute or relative)
    new_strip = strip + 1 
    striped_path = line.split(os.sep)
    tmp_strip = striped_path[new_strip:]
    new_path = os.sep.join(tmp_strip)
    return new_path

class FileStream:
    """
    Configuration of the file and initial file methods.
    """

    def __parse_strip(self,default,line):
        """
        Parse the value from the command line. The method parses the file and strip value. 

        Parameter:
            - default - default strip value
            - line - line to process

        Return: the tuple with file and value. The method throws exception in the case of any error
        """
        fList = line.split(":")
        if len(fList) > 3:
            raise RuntimeError("Invalid format of the file with strip")
        if len(fList) == 1:
            return (fList[0],default)
        
        # The passed value is 2, parse values
        strip = int(fList[1])
        if(strip < 0):
            raise ValueError("Strip value cannot be negative")

        return (fList[0],strip)

    def __init__(self,line,default,debug):
        """
        Initilization of the stip value for the given file

        Parameters:
            - line - line to process
            - default - default indent
            - debug - enable debug mode
        """
        # Parse the line data
        tmp = self.__parse_strip(default,line)
        self.__file  = tmp[0]
        self.__strip = tmp[1]

        # Load lines into the list
        tmpF = open(self.__file,'r')
        self.__lines = [f.strip() for f in tmpF.readlines() if not f.isspace()]
        tmpF.close()

        # Check if the file contains any data
        if len(self.__lines) == 0:
            raise RuntimeError("No content was detected inside {} format".format(self.__file))

        # Extract strip value if it is defined
        tmp_strip = self.__lines[0]
        if tmp_strip.startswith("STRIP="):
            # It seems that we have a strip command, parse the value
            tmp_strip = tmp_strip.replace("STRIP=","")
            self.__strip = int(tmp_strip)
            # Remove the first line from the analyzed set
            self.__lines.pop(0)
        
        # Check the strip value
        if self.__strip < 0:
            raise ValueError("Strip value cannot be negative!")

        # Prepare the set which will be used for probing
        s_lines = [strip_line(f, self.__strip) for f in self.__lines]
        self.__fset = set(s_lines)

        # Print debug information
        if debug:
            print("\n\n","*"*100,"\n\n")
            print("Adding file {} (stripped):".format(self.__file))
            for s_line in s_lines:
                print("-> ", s_line)
            print("File processing done ...")

    @property
    def file(self):
        """
        Get the file
        """
        return self.__file

    @property
    def strip(self):
        """
        Get the strip value
        """
        return self.__strip

    @property
    def lines(self):
       """
       Get loaded lines
       """
       return self.__lines

    @property
    def fset(self):
        """
        Get the set which can be used for probing
        """
        return self.__fset

    def __str__(self):
        """
        Get the string representatio of the object
        """
        ret  = "FileStream: {}".format(self.file)
        ret += "\t -strip = {}".format(self.strip)
        ret += "\t -lines = {}".format(self.lines)
        return ret

class AnalyzeFiles:
    """
    Module with the implementation of the analysis algorithm 
    """

    def __init__(self, unique_files, other_files,debug):
        """
        Initilization of the analysis argument

        Parameter:
            - unique_files - list of files with from the uniqueset
            - other_files - list of files from the analyzed set
        """
        self.unique_files = unique_files
        self.other_files  =  other_files

        # Prepare set and unique files for the analysis
        self.unique_list = []
        self.non_unique_list = []

        # Setup the debug flag
        self.debug = debug

    def __str__(self):
        """
        Print the string representation fo the self 
        """
        ret  = ("Analyzer source:\n",
                "\t -unique_files={}\n".format(str(self.unique_files)),
                "\t -other_files={}\n".format(str(self.other_files))
                )
        return ''.join(ret)

    def ___is_in_fsets(self,line):
        """
        Search all available other sets for the given line.

        Parameters:
            - line - line to analyze

        Return: True iff the file is in the list, False otherwise
        """
        for fother in self.other_files:
            if line in fother.fset:
                if self.debug:
                    print("===> Match: {} found in {}".format(line,fother.file))

                return True

        return False

    def analyze(self):
        """
        Start the analysis of files in the unique set
        """
        # Take a file from the unique set and analyze it with the rest of files. 
        # Concatenate all unique files
        for uniqf in self.unique_files:
            # In the beginning, all files are appended and considered unique
            striped_lines = [strip_line(f,uniqf.strip) for f in uniqf.lines]
            self.unique_list.extend(striped_lines)
            banned_idx = []

            # Take each file from the set, strip it and try to find it in each other_files.
            # The strip value is taken from the uniqf object (type FileStream)
            for idx in range(len(self.unique_list)):
                res_line = self.unique_list[idx]

                # Check if the file is in all remaining file sets.
                # - yes - add it into the non-unique one and remove it from the unique one
                # - no  - let it in the unique set 
                if self.___is_in_fsets(res_line):
                    # Print debug information
                    if self.debug:
                        print("=> Removing {} from the unique set".format(res_line))

                    self.non_unique_list.append(res_line)
                    banned_idx.append(idx)

            # Remove banned indexes (reverse the list and remove from the end)
            banned_idx.reverse()
            for idx in banned_idx:
                self.unique_list.pop(idx)

        # Make list unique
        self.unique_list = list(set(self.unique_list))
        self.non_unique_list =  list(set(self.non_unique_list))

        # Sort results
        self.unique_list.sort()
        self.non_unique_list.sort()

    # Number of stars in the box
    BOX_STARS=100

    def __print_box(self,text):
        """
        Print box from '='

        Parameters:
            - text - printed text
        """
        print(AnalyzeFiles.BOX_STARS * "=")
        print("= ",text)
        print(AnalyzeFiles.BOX_STARS * "=")

    def print_results(self):
        """
        Print results of the analysis
        """
        self.__print_box("Unique set ")
        for i in self.unique_list:
            print("\t--> {}".format(i))

        print("\n"*5)

        self.__print_box("Non-unique set")
        for i in self.non_unique_list:
            print("\t--> {}".format(i))
