import os

root = os.path.abspath(__file__)
for _ in xrange(3):
    root = os.path.dirname(root)

def get_path(path):
    return os.path.join(root, path)