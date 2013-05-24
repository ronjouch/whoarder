#!/usr/bin/python3

import argparse

if __name__ == '__main__':

    # Boilerplate to allow running as script directly. Avoids error below:
    # SystemError: Parent module '' not loaded, cannot perform relative import
    # See http://stackoverflow.com/questions/2943847/nightmare-with-relative-imports-how-does-pep-366-work/6655098#6655098
    if __package__ is None:
        import sys
        import os
        abspath = os.path.abspath(__file__)
        parent_dir = os.path.dirname(os.path.dirname(abspath))
        sys.path.insert(0, parent_dir)
        from clippings import Clippings
        del sys, os

    parser = argparse.ArgumentParser(description="whoarder converts Kindle \
                        'My Clippings.txt' files to more pleasant HTML.")
    parser.add_argument('source',
                        help='Path to the source file, stored by Kindle in \
                        /Media/Kindle/documents/My Clippings.txt.')
    parser.add_argument('destination',
                        help='Target HTML file. If omitted, a .html bearing \
                        the same name as the input .txt file will be used.',
                        nargs='?', default=None)
    args = parser.parse_args()

    clippings = Clippings(args.source, args.destination)
    clippings.export_clippings()
    print('Successfully wrote ' + clippings.dest + "\n")
