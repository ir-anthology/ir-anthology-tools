#!/usr/bin/env python3

import os
from pathlib import Path
import glob


def check_args():
    # TODO: check for alternative directory parameter
    return True


def usage():
    print(f'Usage: {os.path.basename(__file__)} [path-to-wcsp15-bibfiles]')


def get_next_bibfile():
    # go through subdirectories
    for filename in glob.iglob(f'{wcsp15_bibfile_dir}**/*.bib', recursive=True):
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


def save_bibfile_data(text: str, doi: str):
    prefix = 'unknown'
    if doi:
        separator_pos = doi.find('/')
        prefix = doi[:separator_pos]
    with open(f'{wcsp15_out_dir}{prefix}.bib', 'a', encoding='utf-8') as output_bibfile:
        output_bibfile.write(f'{text}\n')


wcsp15_bibfile_dir = '/mnt/ceph/storage/data-in-production/ir-anthology/tmp/wcsp15/webis-csp-corpus/bib/'
wcsp15_out_dir = '/mnt/ceph/storage/data-in-production/ir-anthology/tmp/wcsp15/'

if __name__ == '__main__':
    check_args() or usage()
    for input_bibfile in get_next_bibfile():
        print(input_bibfile)
        text, doi, bib_found = extract_bib_contents(input_bibfile)
        if bib_found:
            save_bibfile_data(text, doi)
        else:
            print(f'↳ NO DATA')
