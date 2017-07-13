'''
Author: Mutti K

Little helper script for when you need to grep a bunch of files
and want pretty results.
Results are in html and clickable filenames.

Note: full grep parameters not support on osx.
Tested on linux

TODO:
Condense results
'''
from __future__ import print_function
import os
import sys
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(script_path, 'libs'))
from subprocess import call
import getopt
import argparse

settings = {
    'source_code_path' : None,
    'grep_string' : None,
    'results_file' : None,
    'results_file2' : None,
    'results_file3' : None,
}

def main():
    parser = argparse.ArgumentParser(
                description="Helper script for grepping files and reading results in html."
            )
    parser.add_argument('--grep_string',
                required=True,
                help="Search string")
    parser.add_argument('--source_code_path',
                required=True,
                help="Path to search")
    parser.add_argument('--results_file',
                required=True,
                help="Results file")
    args = parser.parse_args()
    settings.update(vars(args))

    settings['results_file2'] = settings['results_file'] + '.tmp'
    settings['results_file3'] = settings['results_file2'] + '.3'

    settings['source_code_path'] = os.path.abspath(settings['source_code_path'])
	#Unsafe having shell=True
    '''
    Grep for string and list 3 lines before and after.
    Parse results through aha for html formatting
    '''
    grep_command = 'grep -inIEr -C 3 --color=ALWAYS "{}" {} | aha > {}' \
        .format(settings['grep_string'],
            settings['source_code_path'],
            settings['results_file3'],)

    # Convert full path names to a tag with tooltip displaying full path
    perl_command1 = "perl -pe 's/>(\\/.*?)\\/([\\w|.]*?)</><a title=\"\\1\\/\\2\" href=\"\\1\\/\\2\">\\2<a></g' {} > {}"\
        .format(settings['results_file3'],
            settings['results_file2'],)

    # Add surrounding span on findings
    perl_command2 = "perl -0777 -pe 's/(<span)(.*?--<\\/span>)/<span class=\"finding\">\\1\\2<\\/span>/smg' {} > {}"\
        .format(settings['results_file2'],
            settings['results_file'],)

    call(grep_command,shell=True)
    call(perl_command1,shell=True)
    call(perl_command2,shell=True)

if __name__=='__main__':
    try:
        main()
    except Exception as e:
        print('Cannot run program.\n%s' %e)
        sys.exit(0)
