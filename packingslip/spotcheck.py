#!/usr/bin/env python
"""
Take a list of files and a directory.
Take a hash of each file provided and look for a corresponding file in
the directory.  Take a hash of that and compare.
"""

import argparse
import os
import subprocess
import sys


def GetHash(filepath):
    """
    returns (hash, filename)
    """
    try:
        p = subprocess.Popen(['sha1sum', filepath],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, _ = p.communicate()
    except:
        raise
    out_str = out.encode('utf-8')
    if p.returncode != 0:
        return None
    return out_str.split()[0]


def main(args):
    files = args.files[:-1]
    dir = args.files[-1:][0]
    assert os.path.isdir(dir)
    basename_to_path = dict([(os.path.basename(f), f) for f in files])
    local_hashs = dict([(n, GetHash(basename_to_path[n]))
                        for n in basename_to_path])
    remote_bname_to_path = {}
    for bname in basename_to_path:
        remote_fpath = os.path.join(dir, bname)
        remote_bname_to_path[bname] = remote_fpath
    remote_hashs = dict([(n, GetHash(remote_bname_to_path[n]))
                         for n in remote_bname_to_path])
    for bname in local_hashs:
        local_hash = local_hashs[bname]
        remote_path = remote_bname_to_path[bname]
        remote_hash = remote_hashs[bname]
        print('{:40} | {:40}'.format(bname, remote_path))
        print('{:40} | {:40}'.format(local_hash, remote_hash))


def dispatch_main():
    parser = argparse.ArgumentParser(prog='spotcheck')
    parser.add_argument('files', nargs='+',
                         help='Files followed by a directory')
    args = parser.parse_args(sys.argv[1:])
    main(args)


if __name__ == '__main__':
    dispatch_main()
