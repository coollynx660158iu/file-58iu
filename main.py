We need to write a small Python project that deduplicates files. Requirements: single file, under 60 lines, short module docstring, standard library only, include a __main__ block. So we can write a script that takes a directory path, scans for duplicate files by size and hash, and optionally delete duplicates or print them. Under 60 lines. We can keep it simple: read file list, group by size, compute hash for each group if size same, then find duplicate groups and print them. Provide command-line arguments: path, maybe --delete to delete duplicates (keep first). We'll aim for 50 lines. Include shebang maybe optional. But can just have docstring top.

We need to have a short module docstring. Let's do:

"""File deduplication utility: find duplicate files by size and content hash."""

Ok.

Implementation: use argparse for CLI. Use os.walk to gather files. Use collections defaultdict. Use hashlib. Provide main function.

Line count: we need to count lines. Let's draft.

Line 1: module docstring.

Line 2: import os, sys, hashlib, argparse, collections.

We'll need to define main function.

Better to try to keep lines minimal.

Let's draft:

"""File deduplication utility: find duplicate files by size and content hash."""

import os, sys, argparse, hashlib
from collections import defaultdict

def file_hash(path, block=65536):
    h=hashlib.sha1()
    try:
        with open(path,'rb') as f:
            while chunk:=f.read(block):
                h.update(chunk)
    except Exception as e:
        return None
    return h.hexdigest()

def find_dups(root):
    size_map=defaultdict(list)
    for dirpath,_,filenames in os.walk(root):
        for name in filenames:
            p=os.path.join(dirpath,name)
            try:
                sz=os.path.getsize(p)
            except OSError:
                continue
            size_map[sz].append(p)
    dups=[]
    for sz,paths in size_map.items():
        if len(paths)<2: continue
        hash_map=defaultdict(list)
        for p in paths:
            h=file_hash(p)
            if h:
                hash_map[h].append(p)
        for h,plist in hash_map.items():
            if len(plist)>1:
                dups.append(plist)
    return dups

def main():
    parser=argparse.ArgumentParser(description="Deduplicate files.")
    parser.add_argument('path',help='directory to scan')
    parser.add_argument('-d','--delete',action='store_true',help='delete duplicates, keep first')
    args=parser.parse_args()
    dups=find_dups(args.path)
    if not dups:
        print("No duplicates found.")
        return
    for group in dups:
        print("Duplicate group:")
        for p in group:
            print("  ",p)
    if args.delete:
        for group in dups:
            keep=group[0]
            for dup in group[1:]:
                try:
                    os.remove(dup)
                    print(f"Deleted {dup}")
                except OSError as e:
                    print(f"Failed {dup}: {e}")

if __name__=="__main__":
    main()

Count lines.

Let's count:

1: module docstring
3: import line
4: from collections import...
6: def file_hash...
7: h=...
8: try...
9: with open...
10: while...
11: h.update...
12: except...
13: return None
14: return h.hexdigest()
16: def find_dups...
17: size_map=...
18: for dirpath...
19: for name...
20: p=os.path.join...
21: try:
22: sz=os.path.getsize...
23: except...
24: continue
25: size_map[sz].append(p)
26: dups=[]
27: for sz,paths...
28: if len(paths)<2: continue
29: hash_map=...
30: for p in paths:
31: h=file_hash(p)
32: if h:
33: hash_map[h].append(p)
34: for h,plist...
35: if len(plist)>1:
36: dups.append(plist)
37: return dups
39: def main():
40: parser=...
41: parser.add_argument...
42: parser.add_argument...
43: args=parser.parse_args()
44: dups=find_dups(args.path)
45: if not dups:
46: print...
47: return
48: for group in dups:
49: print...
50: for p in group:
51: print...
52: if args.delete:
53: for group in dups:
54: keep=group[0]
55: for dup in group[1:]:
56: try:
57: os.remove(dup)
58: print...
59: except OSError as e:
60: print...
62: if __name__=="__main__":
63: main()

We have 63 lines. Need under 60. We can reduce lines by merging logic or fewer prints. For instance, remove keep variable unused. Combine prints. Maybe remove the keep assignment. Also we can reduce error handling prints. Let's condense.

Also we can remove print of duplicate group heading maybe. But must show group. But we could compress code. Also we can inline some lines.

Let's optimize.

Line 1: docstring

Line 2: imports all at once: import os, sys, argparse, hashlib, collections

But collections not needed if we use defaultdict import. But we can use from collections import defaultdict. Keep.

Let's rewrite quickly under 60 lines.

We'll write:

"""File deduplication utility: find duplicate files by size and hash."""

import os, argparse, hashlib
from collections import defaultdict

def hsh(p,block=65536):
    h=hashlib.sha1()
    try:
        with open(p,'rb') as f:
            while b:=f.read(block): h.update(b)
    except: return None
    return h.hexdigest()

def dups(root):
    s=defaultdict(list)
    for d,_,f in os.walk(root):
        for n in f:
            p=os.path.join(d,n)
            try: s[os.path.getsize(p)].append(p)
            except: pass
    res=[]
    for sz,ps in s.items():
        if len(ps)>1:
            h=defaultdict(list)
            for p in ps:
                hp=hsh(p)
                if hp: h[hp].append(p)
            for group in h.values():
                if len(group)>1: res.append(group)
    return res

def main():
    a=argparse.ArgumentParser()
    a.add_argument('path')
    a.add_argument('-d','--delete',action='store_true')
    args=a.parse_args()
    for g in dups(args.path):
        print('Duplicate group:', g)
        if args.delete:
            for d in g[1:]:
                try: os.remove(d)
                except: pass
                print('Deleted', d)

if __name__=='__main__': main