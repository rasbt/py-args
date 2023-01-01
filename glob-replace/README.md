# glob-replace

A Python command line tool for global replacements of strings in text-formatted files in a single directory or directory tree.

<br>
<br>

## Sections
- [Examples](#examples)
- [Usage](#usage)
- [Changelog](#changelog)

<br>
<br>

## Examples
[[back to top](#sections)]

The `glob-replace` utility script can come in handy for replacing certain words or phrases in a collection of files. For example, if you are interested in bumping a "Copyright 2013-2022" to "Copyright 2013-2023" on your personal website or code repository.

I recommend doing this in 3 steps:

**Step 1: Create a backup**

Make a copy of the target folder (for the just-in-case scenario).

```bash
rsync -avP personal-website ~/Desktop/personal-website-backup
```

**Step 2: Dry run**

Run the replacement command using the `--print` flag, which just prints the files it would change.

```bash
python glob-replace.py personal-website --walk --search "2013-2022" --replace "2013-2023" --print 
```

**Step 3: Apply the changes**

Run the replacement command without the `--print` flag to make the actual changes.

```python
python glob-replace.py personal-website --walk --search "2013-2022" --replace "2013-2023"
```



<br>
<br>

## Usage
[[back to top](#sections)]

An overview of all command line arguments.


<pre>./glob-replace.py -h
usage: glob-replace.py [-h] [-s SEARCH] [-r REPLACE] [-w] [-e EXTENSIONS] [-p]
                       [-v]
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
  -f REPLACE_FROM_FILE, --replace_from_file REPLACE_FROM_FILE
                      Link to a text file that contains the text to replace the query with
  -w, --walk            Applies the global replacement recursively to sub-directorires.
  -e EXTENSIONS, --extensions EXTENSIONS
                        Only process files with particular extensions. Comma separated, e.g., ".txt,.py"
  -b, --skip_binary     Skips binary files if enabled (may result in false 
                        positives and negatives).
  -p, --print           Prints what it would rename.
  -v, --version         show program's version number and exit</pre>


<br>
<br>

## Changelog
[[back to top](#sections)]

### v1.3
- Adds an option to read the string that is used for replacement from an external text file.

### v1.2
- Adds an optional `-b` (`--skip_binary`) flag to skip binary files.

### v1.1
- Adds an optional `-p` (`--print`) flag to  print out the number of replacements that `glob-replace.py` would make instead of actually replacing those strings.