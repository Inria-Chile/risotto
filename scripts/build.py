import sys
from pathlib import Path
from nbdev.export import notebook2script

sys.path.append(".")


def main():
    notebook2script()
    sys.exit(0)


if __name__ == "__main__":
    main()
