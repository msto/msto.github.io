#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 Matthew Stone <mstone5@mgh.harvard.edu>
# Distributed under terms of the MIT license.

"""

"""

import argparse
from _scripts.parse_pubmed import scrape_pubmed


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('pubmed_ids', type=argparse.FileType('r'))
    parser.add_argument('citations', type=argparse.FileType('w'))
    args = parser.parse_args()

    args.citations.write("---\nlayout: page\ntitle: Publications & Preprints\n"
                         "permalink: /publications/\n---\n")

    pmids = [p.strip() for p in args.pubmed_ids.readlines()]
    citations = scrape_pubmed(pmids)

    for i, citation in enumerate(citations):
        idx = len(citations) - i
        citation = "{0}. {1}".format(idx, citation)
        if i < len(citations) - 1:
            args.citations.write(citation + '\n\n')
        else:
            args.citations.write(citation + '\n')

    args.citations.write('{: reversed="reversed"}')


if __name__ == '__main__':
    main()
