#runs when using "python -m pwCheck"
#calls main from cli.py

import sys
from pwCheck.cli import main

if __name__ == "__main__":
    sys.exit(main())

    