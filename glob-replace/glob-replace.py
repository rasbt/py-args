#!/usr/bin/env python

# Sebastian Raschka 2014
# A command line tool for global replacements of strings in files.

import glob
import fileinput
import sys
import os

searched_files = 0
replaced_instances = 0 

def check_extension(extensions, filename):
    for x in extensions:
        if filename.endswith(x):
            return True
    return False

def replace_indir(extensions, search, replace, cur_dir, print_out):
    filenames = glob.glob(os.path.join(cur_dir,'*'))
    global searched_files
    global replaced_instances
    for f in filenames:
        found = 0
        if not os.path.isfile(f):
            continue
        if not extensions or check_extension(extensions, f):
            if print_out:
                with open(f, 'r') as in_file:
                    for line in in_file:
                        if search in line:
                            found += 1
            else:
                for line in fileinput.input(f, inplace=True):
                    if search in line:
                        found += 1
                    sys.stdout.write(line.replace(search, replace))
        
        replaced_instances += found
        searched_files += 1
        if print_out and found:
            print('%d x in %s' % (found, f))

def run(extensions, search, replace, cur_dir, recursive, print_out):
    if recursive:
        tree = os.walk(cur_dir)
        for d in tree:
            replace_indir(extensions, search, replace, cur_dir=d[0], print_out=print_out)
    else:
        replace_indir(extensions, search, replace, cur_dir=cur_dir, print_out=print_out)  
		
		
if __name__ == '__main__':
    
    import argparse

    parser = argparse.ArgumentParser(
        description='A command line tool for global replacements of strings in files.',
        formatter_class=argparse.RawTextHelpFormatter
        )


    parser.add_argument('start_dir')

    parser.add_argument('-s', '--search', help='String to be replaced.')
    parser.add_argument('-r', '--replace', help='String to replace the search query with.')
    parser.add_argument('-w', '--walk', action='store_true', default=False, help='Applies the global replacement recursively to sub-directorires.')
    parser.add_argument('-e', '--extensions', help='Only process files with particular extensions. Comma separated, e.g., ".txt,.py"')
    parser.add_argument('-p', '--print', action='store_true', help='Prints what it would rename.')
    parser.add_argument('-v', '--version', action='version', version='v. 1.1')

    args = parser.parse_args()

    extensions = False
    if args.extensions:
        extensions = args.extensions.split(',')
        
    run(extensions, args.search, args.replace, args.start_dir, args.walk, args.print)    

    would = 'replaced'
    if args.print:
        would = 'would replace'

    print('Searched %s file(s) and %s %s instance(s) of %s' %(searched_files, would, replaced_instances, args.search))
