# glob-replace

A Python command line tool for global replacements of strings in text-formatted files in a single directory or directory tree.

<br>
<br>

## Example

An example of replacing all instances of a string 'World' by another string 'Earth' in all .txt files in a directory tree:

	./glob-replace.py ./testdir -s World -r Earth -e .txt -w
	Searched 6 file(s) and replaced 6 instance(s) of World

![](./images/img_1.png)


<br>
<br>

## Usage

An overview of all command line arguments.


<pre>./glob-replace.py -h
usage: glob-replace.py [-h] [-s SEARCH] [-r REPLACE] [-w] [-e EXTENSIONS] [-v]
                       start_dir

A command line tool for global replacements of strings in files.

positional arguments:
  start_dir

optional arguments:
  -h, --help            show this help message and exit
  -s SEARCH, --search SEARCH
                        String to be replaced.
  -r REPLACE, --replace REPLACE
                        String to replace the search query with.
  -w, --walk            Applies the global replacement recursively to sub-directorires.
  -e EXTENSIONS, --extensions EXTENSIONS
                        Only process files with particular extensions. Comma separated, e.g., ".text,.py"
  -v, --version         show program's version number and exit</pre>