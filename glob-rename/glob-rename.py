#!/usr/bin/env python

# Sebastian Raschka 2014-2018
# A command line tool for global replacements of strings in files.

import glob
import os
import shutil

checked_files = 0
renamed_files = 0
checked_dirs = 0
renamed_dirs = 0


def check_extension(extensions, filename):
    for x in extensions:
        if filename.endswith(x):
            return True
    return False


def replace_indir(extensions, search, replace,
                  cur_dir, print_out):
    filenames = glob.glob(os.path.join(cur_dir, '*'))
    global checked_files
    global renamed_files
    for f in filenames:
        # for some reason (bug in glob?)
        # directories sometimes end up here;
        # hence the check on the next line
        if not os.path.isfile(f):
            continue
        else:
            if not extensions or check_extension(extensions, f):
                if search in f:

                    # replace
                    old_file = os.path.basename(f)

                    if replace == '<lowercase>':
                        new_file = os.path.basename(f).lower()
                    elif replace == '<uppercase>':
                        new_file = os.path.basename(f).upper()
                    else:
                        new_file = os.path.basename(f).replace(search, replace)

                    if old_file != new_file:
                        new_path = os.path.join(os.path.dirname(f), new_file)
                        if not print_out:
                            os.rename(f, new_path)
                        else:
                            print('%s --> %s' % (f, new_path))
                        renamed_files += 1
                checked_files += 1


def rename_dir(search, replace,
               cur_dir, print_out):
    global checked_dirs
    global renamed_dirs
    if not os.path.isdir(cur_dir):
        return

    old_dir_base = os.path.basename(cur_dir)

    if replace == '<lowercase>':
        new_dir = old_dir_base.lower()
    elif replace == '<uppercase>':
        new_dir = old_dir_base.upper()
    else:
        new_dir = old_dir_base.replace(search, replace)

    if old_dir_base != new_dir:
        new_path = os.path.join(os.path.dirname(cur_dir), new_dir)
        if not print_out:
            shutil.move(cur_dir, new_dir)
        else:
            print('%s --> %s' % (cur_dir, new_path))
        renamed_dirs += 1
    checked_dirs += 1


def run(extensions, search, replace, cur_dir,
        recursive, print_out, directories):
    if recursive:
        tree = os.walk(cur_dir)
        for d in tree:
            replace_indir(extensions, search, replace,
                          cur_dir=d[0], print_out=print_out)

    else:
        replace_indir(extensions, search, replace,
                      cur_dir=cur_dir, print_out=print_out)

    if directories:
        if recursive:
            tree = os.walk(cur_dir)
            tree_contents = [d for d in tree]
            tree_contents = tree_contents[::-1]
            for d in tree_contents:
                rename_dir(search, replace,
                           cur_dir=d[0], print_out=print_out)

    else:
        rename_dir(search, replace,
                   cur_dir=cur_dir, print_out=print_out)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(
        description='A command line tool for global renaming of files.',
        formatter_class=argparse.RawTextHelpFormatter
        )

    parser.add_argument('start_dir')

    parser.add_argument('-s', '--search', default='', help=(
        'String to be replaced (default:"").'))
    parser.add_argument('-r', '--replace', help=(
        'String to replace the search query with.\nOther '
        'options: "<lowercase>", "<uppercase>" .'))
    parser.add_argument('-w', '--walk', action='store_true',
                        default=False, help=(
                            'Applies the global replacement '
                            'recursively to sub-directorires.'))
    parser.add_argument('-d', '--directories', action='store_true',
                        default=False, help=('Rename directories as well.'))
    parser.add_argument('-e', '--extensions', help=(
        'Only process files with particular extensions. Comma separated,'
        ' e.g., ".txt,.py"'))
    parser.add_argument('-p', '--print', action='store_true', help=(
        'Prints what it would rename.'))
    parser.add_argument('-v', '--version',
                        action='version', version='v. 1.1')

    args = parser.parse_args()

    extensions = False
    if args.extensions:
        extensions = args.extensions.split(',')

    run(extensions, args.search, args.replace,
        args.start_dir, args.walk, args.print, args.directories)

    would = 'renamed'
    if args.print:
        would = 'would rename'
    print('Checked %s files and %s %s file(s).' % (
        checked_files, would, renamed_files))

    if args.directories:
        print('Checked %s directories and %s %s dir(s).' % (
            checked_dirs, would, renamed_dirs))
