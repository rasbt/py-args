#!/usr/bin/env python

# Sebastian Raschka 2014
# A command line tool for global replacements of strings in files.

import glob
import fileinput
import sys
import os

checked_files = 0
renamed_instances = 0 

def check_extension(extensions, filename):
    for x in extensions:
        if filename.endswith(x):
            return True
    return False

def replace_indir(extensions, search, replace, cur_dir, print_out):
    filenames = glob.glob(os.path.join(cur_dir,'*'))
    global checked_files
    global renamed_instances
    for f in filenames:
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
                        print('%s --> %s' %(f, new_path))
                    renamed_instances += 1         
            checked_files += 1

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
        description='A command line tool for global renaming of files.',
        formatter_class=argparse.RawTextHelpFormatter
        )


    parser.add_argument('start_dir')

    parser.add_argument('-s', '--search', default='', help='String to be replaced (default:"").')
    parser.add_argument('-r', '--replace', help='String to replace the search query with.\nOther options: "<lowercase>", "<uppercase>" .')
    parser.add_argument('-w', '--walk', action='store_true', default=False, help='Applies the global replacement recursively to sub-directorires.')
    parser.add_argument('-e', '--extensions', help='Only process files with particular extensions. Comma separated, e.g., ".txt,.py"')
    parser.add_argument('-p', '--print', action='store_true', help='Prints what it would rename.')
    parser.add_argument('-v', '--version', action='version', version='v. 1.0.2')

    args = parser.parse_args()

    extensions = False
    if args.extensions:
        extensions = args.extensions.split(',')
        
    run(extensions, args.search, args.replace, args.start_dir, args.walk, args.print)    

    would = 'renamed'
    if args.print:
        would = 'would rename'
    print('Checked %s items and %s %s files(s).' %(checked_files, would, renamed_instances))

