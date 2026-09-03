# __main__.py
# 
# When this module is called as a standalone program, it take in command line
#    arguments from user and pass them to huffmanEncoder.py.
# 
# Creator: Sean Dickson

from pathlib import Path
import argparse

from huffmanEncoder.huffmanEncoder import process_files

# Build required arguments to be passed in by user
arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("action", type=str, help="'encode'/'decode'")
arg_parser.add_argument("in_file", type=str, help="Input File Pathname")
arg_parser.add_argument("out_file", type=str, help="Output File Pathname")
arg_parser.add_argument("freq_table", type=str, help="Frequency Table Pathname")
args = arg_parser.parse_args()

# Determine if task is "encoding" or "decoding"
action = str(Path(args.action))
encode = False
if action.lower() not in ['encode', 'decode']:
    raise Exception('Must specify either "encode" or "decode"!')
elif action.lower() == 'encode':
    encode = True

# Find path for given I/O files and frequency table file
in_path = Path(args.in_file)
out_path = Path(args.out_file) 
freq_table_path = Path(args.freq_table)

# Try calling 'process_files' function from huffmanEncoder.py
try:
    with in_path.open('r') as input_file, out_path.open('w') as output_file, freq_table_path.open('r') as table_file:
        process_files(encode, input_file, output_file, table_file)
        
# If input file is not found, throw FileNotFoundError
except FileNotFoundError:
    print(f"Either '{in_path}' or '{freq_table_path}' was not found. Try again!")