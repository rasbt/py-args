#!/usr/bin/env python

# Sebastian Raschka 2014-2018
# A command line tool for global replacements of strings in files.

import glob
import fileinput
import sys
import os


searched_files = 0
replaced_instances = 0

TEXTCHARS = bytearray({7, 8, 9, 10, 12, 13, 27} |
                      set(range(0x20, 0x100)) - {0x7f})


def check_extension(extensions, filename):
    for x in extensions:
        if filename.endswith(x):
            return True
    return False


def is_binary(filepath):
    with open(filepath, 'rb') as f:
        content = f.read(1024)
    return bool(content.translate(None, TEXTCHARS))


def replace_indir(extensions, search, replace,
                  cur_dir, print_out, skip_binary):
    filenames = glob.glob(os.path.join(cur_dir, '*'))
    global searched_files
    global replaced_instances
    for f in filenames:

        found = 0
        if not os.path.isfile(f):
            continue

        if skip_binary:
            if is_binary(f):
                searched_files += 1
                continue
        if not extensions or check_extension(extensions, f):
            if print_out:
                with open(f, 'r', encoding="ISO-8859-1") as in_file:
                    try:
                        for line in in_file:
                            if search in line:
                                found += 1
                    except UnicodeDecodeError as e:
                        print('ERROR: File %s may be binary. You can try to'
                              ' skip binary by using the --skip_binary flag' %
                              f)
                        raise e

            else:
                for line in fileinput.input(f, inplace=True, mode='rU'):
                    if search in line:
                        found += 1
                    try:
                        sys.stdout.write(line.replace(search, replace))
                    except UnicodeDecodeError as e:
                        print('ERROR: File %s may be binary. You can try to'
                              ' skip binary by using the --skip_binary flag' %
                              f)
                        raise e

        replaced_instances += found
        searched_files += 1
        if print_out and found:
            print('%d x in %s' % (found, f))


def run(extensions, search, replace, cur_dir,
        recursive, print_out, skip_binary):
    if recursive:
        tree = os.walk(cur_dir)
        for d in tree:
            replace_indir(extensions, search, replace,
                          cur_dir=d[0], print_out=print_out,
                          skip_binary=skip_binary)
    else:
        replace_indir(extensions, search, replace,
                      cur_dir=cur_dir, print_out=print_out,
                      skip_binary=skip_binary)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description=('A command line tool for global '
                     'replacements of strings in files.'),
        formatter_class=argparse.RawTextHelpFormatter
        )

    parser.add_argument('start_dir')

    parser.add_argument('-s', '--search', help='String to be replaced.')
    parser.add_argument('-r', '--replace', help='String to replace the search '
                        'query with.')
    parser.add_argument('-f', '--replace_from_file', help='Link to a text '
                        'file that contains the text to replace the'
                        ' query with')
    parser.add_argument('-w', '--walk', action='store_true', default=False,
                        help='Applies the global replacement recursively to '
                        'sub-directorires.')
    parser.add_argument('-e', '--extensions', help='Only process files with '
                        'particular extensions. '
                        'Comma separated, e.g., ".txt,.py"')
    parser.add_argument('-p', '--print', action='store_true',
                        help='Prints what it would rename.')
    parser.add_argument('-b', '--skip_binary', action='store_true',
                        help=('Skips binary files if enabled '
                              '(may result in false positives'
                              ' and negatives).'))
    parser.add_argument('-v', '--version', action='version', version='v. 1.1')

    args = parser.parse_args()

    if args.replace and args.replace_from_file:
        raise AttributeError("Can't have both -r/--replace and "
                             "--replace_from_file/-f flags at the same time.")

    if args.replace:
        replace = args.replace
    elif args.replace_from_file:
        with open(args.replace_from_file, 'r', encoding="ISO-8859-1") as f:
            replace = f.read()
    else:
        raise AttributeError("Must use either the -r/--replace or "
                             "--replace_from_file/-f flag.")

    extensions = False
    if args.extensions:
        extensions = args.extensions.split(',')

    run(extensions, args.search, replace,
        args.start_dir, args.walk, args.print, args.skip_binary)

    would = 'replaced'
    if args.print:
        would = 'would replace'

    print('Searched %s file(s) and %s %s instance(s) of %s' % (
          searched_files, would, replaced_instances, args.search))
