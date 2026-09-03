# __main__.py
# 
# When this module is called as a standalone program, it take in command line
#    arguments from user and pass them to multiSorter.py.
# 
# Creator: Sean Dickson

from pathlib import Path
import argparse

from multiSorter.multiSorter import process_files

# Build required arguments to be passed in by user
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("in_path", type=str, help="Input Pathname")
args = arg_parser.parse_args()

# Find path for given I/O files
in_path = Path(args.in_path)
out_path = Path('output_files/' + args.in_path.split('.')[0].split('input_files/')[1] + '-OUTPUT.txt')

# Try calling 'process_files' function from lab3.py
try:
    with in_path.open('r') as input_file, out_path.open('w') as output_file:
        process_files(input_file, output_file)
        
# If input file is not found, throw FileNotFoundError
except FileNotFoundError:
    print(f"Either '{in_path}' or '{out_path}' was not found. Try again!")