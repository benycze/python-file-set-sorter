# Python File Set Analysis

This tool provides a simple analysis of files passed as inputs of the program. The user divides files with strings into two categories:

* Set A - list of files in the first set
* Set B - list of files in the second set

After that, the tool runs the analysis where it takes all elements in the set A (e.g. file contents) and compares them with the set B, where the record from A is added to the:

* Unique set - there is no such record in the set A
* Non-unique set - there is a match in the second B

This tool is just a quickly implemented because I needed to solve this as fast as possible and I didn't know about any suitable tool  which is available online.

**WARNING**: The tool is very simple and it was written in 30 minutes. Therefore, I am actually missing some unit tests and the tool is not guarded against all users input :-).

## Input File Format

The file format contains paths to files (one per a line). There is also a possibilty to specify the `STRIP` value which defines the number of removed path elements from the prefix. For example, the `STRIP=2` applied on `/home/user/abc` results to `abc`. The STRIP value can be passed as the first line of the file or you can specify the strip value as the parameter of passed file like `files.txt:2`. You can also specify the default strip value using the `--strip` parameter. Empty lines are filtered out. 

So, the example of file can be:

```
STRIP=2
/home/user/a/b/c/d.txt
/home/user/a/b/c/x.txt
/home/user/c/d.txt
/home/user/files.txt
/home/user/file.txt
```

Without the `STRIP`:

```
/home/user/a/b/c/d.txt
/home/user/a/b/c/x.txt
/home/user/c/d.txt
/home/user/files.txt
/home/user/file.txt
```

## Example of Usage

You can use this scrip to run the analysis:

```
#!/usr/bin/env bash

python3 sorter.py --unique-files data/input/* --other-files data/others/* $@ | tee output.txt
```

You can get more inforamtion about the tool using the `--help` option:

```
Process two sets of files and search for a unique files in the start group.
The program tries to find a unique files in Set A that are not in the Set B.
The format of input data is a text file where each file is on a line ending
with a \n character. Empty lines are filtered out. The format of unique files
can contain the strip value which removes the first n paths from each analyzed
files. The value can be defined globally or localy per file in the form
FILE:STRIP, where the file is a file path and STRIP is the strip value.The
default value (passed via the --strip argumnet) is assined iff the STRIP value
is not defined. Another possibility is to define a strip value directly in a
file as the first line of the file where the format is STRIP=value, where the
value is a positive integer. The value inside the file has a bigger priority
than value passed by in the argument.

optional arguments:
  -h, --help            show this help message and exit
  --unique-files UNIQUE_FILES [UNIQUE_FILES ...]
                        The set of files which will be analyzed in the unique
                        set (= Set A)
  --other-files OTHER_FILES [OTHER_FILES ...]
                        The set of files which will be analyzed in the non-
                        unique set (= Set B)
  --strip STRIP         Default strip value for all passed files. The default
                        value is 4.
  --debug               Enable the debug mode for the analysis.             Enable the debug mode for the analysis.

```

The tool also contains a stupid code which can be used for the
generation of test files. It generes one file with inputs and second file with randomly selected files (from the first file). I suggest you to edit the file directly to customize it to your needs.