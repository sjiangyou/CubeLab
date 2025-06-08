import os
from pathlib import Path


def find(folder) -> str:
    try:
        if folder == "":
            raise FileNotFoundError
        os.chdir(os.path.expanduser(folder))
        return os.getcwd()
    except FileNotFoundError:
        for root, dirs, files in os.walk(Path.home()):
            if root.endswith("CubeLab"):
                return root


if __name__ == "__main__":
    import sys

    print(find(sys.argv[1]))
