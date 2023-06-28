import os
import platform

def find(folder):
    for root, dirs, files in os.walk(get_user_dir()):
        if root.endswith(folder):
            return os.path.join(root, '')
        
def get_user_dir():
    bases = {'Linux': '/home/', 'Windows': 'C:\\Users\\', 'Darwin': '/Users/'}
    return bases[platform.system()]