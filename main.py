"""
File deduplication utility: list or remove duplicate files in a directory.
"""

import os, hashlib, argparse

def hash_file(path, block=65536):
    h = hashlib.sha256()
    try:
        with open(path, 'rb') as f:
            for b in iter(lambda: f.read(block), b''):
                h.update(b)
    except OSError:
        return None
    return h.hexdigest()

def find_dups(root):
    d = {}
    for dirpath, _, files in os.walk(root):
        for fn in files:
            fp = os.path.join(dirpath, fn)
            h = hash_file(fp)
            if h:
                d.setdefault(h, []).append(fp)
    return [v for v in d.values() if len(v) > 1]

def main():
    p = argparse.ArgumentParser(description='Deduplicate files.')
    p.add_argument('dir', nargs='?', default='.', help='directory to scan')
    p.add_argument('-d', '--delete', action='store_true', help='delete duplicates, keep