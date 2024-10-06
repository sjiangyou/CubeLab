import os


def find(folder) -> str:
    try:
        os.chdir(os.path.expanduser(folder))
        return os.path.join(os.getcwd(), "")
    except FileNotFoundError:
        for root, dirs, files in os.walk(os.path.expanduser("~")):
            if root.endswith("CubeLab/src"):
                return os.path.join(root[:-4], "")


if __name__ == "__main__":
    import sys

    print(find(sys.argv[1]))
