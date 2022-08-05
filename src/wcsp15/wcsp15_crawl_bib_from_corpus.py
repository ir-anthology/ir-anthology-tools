#!/usr/bin/env python3

import os
import sys
import glob
import argparse
from pathlib import Path


DEFAULT_WCSP15_BIB_INPUT_DIR = '/mnt/ceph/storage/data-in-production/ir-anthology/tmp/wcsp15/webis-csp-corpus/bib/'
DEFAULT_WCSP15_BIB_OUTPUT_DIR = '/mnt/ceph/storage/data-in-production/ir-anthology/sources/wcsp15/bibs-by-doi/'


def get_next_bibfile(input_files_dir: str):
    # go through subdirectories
    for filename in glob.iglob(f'{input_files_dir}/**/*.bib', recursive=True):
        yield filename


def extract_bib_contents(bibfile_path: str):
    with open(bibfile_path, encoding='iso8859-1', errors='ignore') as f:
        bibfile_lines = f.readlines()
    acmid = Path(bibfile_path).stem
    bib_before = f'<PRE id="{acmid}">'
    bib_after = '</pre>'
    copy = False
    bib_found = False
    bib_text = []
    doi = ''
    for line in bibfile_lines:
        # check for text between PRE tags
        if bib_after in line:
            copy = False
        if copy:
            bib_text.append(line)
            # try to extract a DOI
            if line.startswith(' doi = '):
                doi = line[8:].replace('},', '').replace('}', '')
        if bib_before in line:
            copy = True
            bib_found = True
    return ''.join(bib_text), doi, bib_found


def save_bibfile_data(text: str, doi: str, output_files_dir: str):
    prefix = 'unknown'
    if doi:
        separator_pos = doi.find('/')
        prefix = doi[:separator_pos]
    with open(os.path.join(output_files_dir, prefix, '.bib'), 'a', encoding='utf-8') as output_bibfile:
        output_bibfile.write(f'{text}\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Takes the WCSP15 bib files and removes surrounding HTML code.')
    parser.add_argument('-i', dest='input_bib_files_directory', required=False, type=str, default=DEFAULT_WCSP15_BIB_INPUT_DIR)
    parser.add_argument('-o', dest='output_bib_files_directory', required=False, type=str, default=DEFAULT_WCSP15_BIB_OUTPUT_DIR)
    args = parser.parse_args()
    if not os.path.isdir(args.input_bib_files_directory):
        print('The input file directory specified does not exist!')
        sys.exit()
    if not os.path.isdir(args.output_bib_files_directory):
        print('The output directory specified does not exist!')
        sys.exit()
    
    for input_bibfile in get_next_bibfile(args.input_bib_files_directory):
        print(input_bibfile)
        text, doi, bib_found = extract_bib_contents(input_bibfile)
        if bib_found:
            save_bibfile_data(text, doi)
        else:
            print(f'↳ NO DATA')
