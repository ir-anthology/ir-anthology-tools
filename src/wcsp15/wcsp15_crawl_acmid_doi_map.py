#!/usr/bin/env python3

import os
import sys
import glob
import json
import argparse


DEFAULT_BIB_INPUT_DIRECTORY = '/mnt/ceph/storage/data-in-production/ir-anthology/sources/wcsp15/bibs-by-doi/'
DEFAULT_MAP_OUTPUT_DIRECTORY = '/mnt/ceph/storage/data-in-production/ir-anthology/sources/wcsp15/'


def get_next_bibfile(input_files_dir: str):
    # go through subdirectories
    for filename in glob.iglob(f'{input_files_dir}*.bib'):
        yield filename


def extract_bib_contents(bibfile_path: str):
    with open(os.path.join(bibfile_path, ''), encoding='utf-8', errors='ignore') as f:
        bibfile_lines = f.readlines()
    
    acmids = []
    acmid = ''
    doi = ''
    for line in bibfile_lines:
        if line.startswith('}'):
            # only if we have both ACMID and DOI, save the pair
            if acmid and doi:
                acmids.append((acmid, doi))
            acmid = ''
            doi = ''
        elif line.startswith(' doi = '):
                doi = line[8:].replace('},', '').replace('}', '').strip()
        elif line.startswith(' acmid = '):
                acmid = line[10:].replace('},', '').replace('}', '').strip()
    return acmids


def save_mapping(acmids, output_directory):
    map_acmid_to_doi = {}
    map_doi_to_acmid = {}
    for pair in acmids:
        map_acmid_to_doi[pair[0]] = pair[1]
        map_doi_to_acmid[pair[1]] = pair[0]

    with open(os.path.join(output_directory, 'acmid2doi.map.json'), 'w', encoding='utf-8') as output_mapfile:
        json.dump(map_acmid_to_doi, output_mapfile)
    with open(os.path.join(output_directory, 'doi2acmid.map.json'), 'w', encoding='utf-8') as output_mapfile:
        json.dump(map_doi_to_acmid, output_mapfile)


if __name__ == '__main__':
    # check arguments
    parser = argparse.ArgumentParser(description='Takes a directory containing bib files with both ACM id and DOI entry, and saves the mappings as JSON files.')
    parser.add_argument('-i', dest='input_bib_files_directory', required=False, type=str, default=DEFAULT_BIB_INPUT_DIRECTORY)
    parser.add_argument('-o', dest='output_map_directory', required=False, type=str, default=DEFAULT_MAP_OUTPUT_DIRECTORY)
    args = parser.parse_args()
    if not os.path.isdir(args.input_bib_files_directory):
        print('The input file directory specified does not exist!')
        sys.exit()
    if not os.path.isdir(args.output_map_directory):
        print('The output directory specified does not exist!')
        sys.exit()
    
    # parse bib files
    acmids = []
    for input_bibfile in get_next_bibfile(args.input_bib_files_directory):
        print(input_bibfile)
        acmids.extend(extract_bib_contents(input_bibfile))
    
    # save mappings
    save_mapping(acmids, output_directory=args.output_map_directory)
