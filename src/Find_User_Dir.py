import os
import platform

def find(name):
    for root, dirs, files in os.walk(get_user_dir()):
        if name in files:
            return os.path.join(root, '')
        
def get_user_dir():
    bases = {'Linux': '/home/', 'Windows': 'C:\\Users\\', 'Darwin': '/Users/'}
    return bases[platform.system()]