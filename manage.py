#!/usr/bin/env python
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app

def run_command(arg):
    if (arg == 'dev' or arg == 'devserver'):
        app.run(debug = True)

def check_args():
    if len(sys.argv) > 1:
        run_command(sys.argv[1])
    else:
        print sys.argv[0] + ' requires an argument. Use --help for more info.'


if __name__ == "__main__":
    check_args()