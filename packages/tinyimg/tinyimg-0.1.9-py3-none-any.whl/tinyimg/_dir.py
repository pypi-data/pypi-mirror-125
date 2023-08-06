import os
from pathlib import Path


class Dir:
    def __init__(self, root: str):
        self.root = root

    def traverse(self, dir_ignore=[]):
        for folder, dirs, files in os.walk(self.root, topdown=True):
            dirs[:] = [d for d in dirs if d not in dir_ignore]
            yield folder, dirs, files

    def exists(self):
        return os.path.exists(self.root)

    def mkdir(self):
        os.makedirs(self.root)

    def get_path(self):
        return Path(self.root)