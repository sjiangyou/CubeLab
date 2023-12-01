import os

def find(folder):
    try:
        os.chdir(os.path.expanduser(folder))
        return os.path.join(os.getcwd(), '')
    except(FileNotFoundError):
        for root, dirs, files in os.walk(os.path.expanduser('~')):
            if(root.endswith('Timer_Project_Files')):
                return os.path.join(root, '')
        
if(__name__ == '__main__'):
    import sys
    print(find(sys.argv[1]))