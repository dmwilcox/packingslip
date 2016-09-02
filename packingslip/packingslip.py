#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Some to-do items:
- handle renames of top level directory, by say removing it from the key, etc.
- if a directory of files only on one side, roll up missing files to be the
  directory on exclusively one side, like git
- do reverse check using hashs to detect renames, and figure how to handle that
- for differences better label what hash came from where
- add verbose mode
- automagically look for index.plist under provided directory, even if not top
  level
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import codecs
import os
import subprocess
import sys
import yaml


DEFAULT_PSLIP_FILE = 'index.pslip'


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
    out_str = out.decode('utf-8')
    if p.returncode != 0:
        return None
    return out_str.split()[0]


def WalkAndHashDir(top_dir):
    hash_dict = {}
    for current_dir, dirs, files in os.walk(top_dir):
        for f in files:
            f_path = os.path.join(current_dir, f)
            f_relpath = os.path.relpath(f_path)
            hash_dict[f_relpath] = GetHash(f_relpath)
    return hash_dict


def CreatePackingSlip(dir, output_pslip=None):
    if not output_pslip:
        output_pslip = os.path.join(dir, DEFAULT_PSLIP_FILE)
    hash_values = WalkAndHashDir(dir)
    with codecs.open(output_pslip, 'w', encoding='utf-8') as f:
        f.write(yaml.dump(hash_values))


def VerifyPackingSlip(packing_slip, dir=None):
    """needs to walk+hash, load a pslip and display a diff"""
    with codecs.open(packing_slip, 'r', encoding='utf-8') as f:
        source_hashs = yaml.load(f.read())
    if not dir:
        dir = os.path.dirname(os.path.abspath(packing_slip))
    dest_hashs = WalkAndHashDir(dir)
    PrintDictDiff(source_hashs, dest_hashs)


def PrintDictDiff(src, dst):
    src_keys = set(src.keys())
    dst_keys = set(dst.keys())
    if not src_keys & dst_keys:
        print('No file paths are common')
        return
    for k in src_keys & dst_keys:
        if src[k] != dst[k]:
            print('{} differs!'.format(k))
            print('{:40} | {:40}'.format(src[k], dst[k]))
        #TODO add printing of identical records under a verbose mode
        #else:
            #print('{} is identical'.format(k))
    exclusively_src = src_keys - dst_keys
    exclusively_dst = dst_keys - src_keys
    if exclusively_src:
        print('Following keys exist only in src:\n{}'.format(
            '\n'.join(exclusively_src))
        )
    if exclusively_dst:
        print('Following keys exist only in dst:\n{}'.format(
            '\n'.join(exclusively_dst))
        )


def create_main(args):
    CreatePackingSlip(args.directory[0])


def verify_main(args):
    VerifyPackingSlip(args.pslip[0])


def main():
    parser = argparse.ArgumentParser(prog='packingslip')
    sub_parsers = parser.add_subparsers(help='sub-command help')

    parser_create = sub_parsers.add_parser('create', help='create help')
    parser_create.add_argument('directory', nargs=1,
                               help='Directory to create a packing slip for.')
    parser_create.set_defaults(func=create_main)

    parser_verify = sub_parsers.add_parser('verify', help='verify help')
    parser_verify.add_argument(
        'pslip',
         nargs=1,
         help='index.pslip file to verify current or specified directory'
    )
    parser_verify.add_argument('--directory',
                               nargs=1,
                               help='Directory to verify against.'
    )
    parser_verify.set_defaults(func=verify_main)

    args = parser.parse_args(sys.argv[1:])
    try:
        args.func(args)
    except AttributeError:
        parser.print_usage()
        sys.exit(1)


if __name__ == '__main__':
    main()
