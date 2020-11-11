from src.transpiler.transpiler import *
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('source', help='Absolute or relative path for the file to transpile.', type=str)
    parser.add_argument('target', help='Absolute or relative path for the file which will be created.', type=str)
    args = parser.parse_args()
    transpile = transpile_file(args.source, args.target)
