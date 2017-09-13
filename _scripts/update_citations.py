#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 Matthew Stone <mstone5@mgh.harvard.edu>
# Distributed under terms of the MIT license.

"""

"""

import itertools
from datetime import datetime
from Bio import Entrez


def parse_pubmed_date(article):
    """
    citation : Bio.Entrez.Parser.CitationElement
    """
    issue = article['MedlineCitation']['Article']['Journal']['JournalIssue']
    pub_date = issue['PubDate']

    if 'Day' not in pub_date:
        fmt = "{year} {month}"
        day = None
    else:
        fmt = "{year} {month} {day}"
        day = issue['PubDate']['Day']

    return fmt.format(year=issue['PubDate']['Year'],
                      month=issue['PubDate']['Month'],
                      day=day)


def parse_pubmed_issue(citation):
    """
    citation : Bio.Entrez.Parser.CitationElement
    """
    issue = citation['Journal']['JournalIssue']

    fmt = "{volume}({issue}):{page}"

    return fmt.format(volume=issue['Volume'],
                      issue=issue['Issue'],
                      page=citation['Pagination']['MedlinePgn'])


def format_pubmed_citation(article):
    """
    article : Bio.Entrez.Parser.DictionaryElement
    """

    # Parse doi
    for data in article['PubmedData']['ArticleIdList']:
        if data.attributes['IdType'] == 'doi':
            doi = str(data)
            doi = '<a href="https://doi.org/{0}">{0}</a>'.format(doi)
        elif data.attributes['IdType'] == 'pubmed':
            fmt = '<a href="https://www.ncbi.nlm.nih.gov/pubmed/{0}">{0}</a>'
            pmid = fmt.format(str(data))

    # get article data
    citation = article['MedlineCitation']['Article']

    def _parse_author(author):
        name = author['LastName'] + ' ' + author['Initials']
        if name == "Stone MR":
            name = "<strong>{0}</strong>".format(name)
        return name

    authors = [_parse_author(author) for author in citation['AuthorList']]
    authors = ', '.join(authors)

    #  title = citation['ArticleTitle'].replace(u'\xa0', ' ').rstrip('.')
    title = citation['ArticleTitle'].rstrip('.')
    journal = citation['Journal']['ISOAbbreviation'].replace('.', '')

    date = parse_pubmed_date(article)
    issue = parse_pubmed_issue(citation)

    # note: trailing doublespace necessary for line break in markdown
    citation = ("{authors}. {title}.<br>  \n"
                "<em>{journal}</em>. {date};{issue}.<br>  \nPMID: {pmid}. DOI: {doi}.")
    citation = citation.format(**locals())

    return citation


def scrape_pubmed(idlist):
    """
    idlist : list of str
        pubmed IDs
    """
    Entrez.email = 'matthew.stone12@gmail.com'
    handle = Entrez.efetch(db='pubmed', retmode='xml', id=','.join(idlist))
    results = Entrez.read(handle)
    articles = results['PubmedArticle']

    def _timestamp(article):
        date = parse_pubmed_date(article)
        if len(date.split()) == 3:
            return datetime.strptime(parse_pubmed_date(article), '%Y %b %d')
        else:
            return datetime.strptime(parse_pubmed_date(article), '%Y %b')

    articles = sorted(articles, key=lambda a: _timestamp(a))[::-1]

    citations = [format_pubmed_citation(article) for article in articles]

    return citations


def get_year(citation):
    return citation.split('</em>. ')[1].split()[0]
    #  return citation.split('\n')[1].split('_. ')[1].split()[0]


def write_citations(citations, fout):
    idx = len(citations)
    citations = sorted(citations, key=get_year)[::-1]

    for year, cites in itertools.groupby(citations, get_year):
        fout.write('### {year}\n'.format(year=year))
        #  fout.write('{{:start="{0}"}}\n'.format(idx))
        fout.write('<ol start="{0}" reversed>\n'.format(idx))

        citelist = []
        for i, cite in enumerate(cites):
            cite = '<li>{0}</li>\n'.format(cite)
            #  cite = '<li>{0}</li><br>\n'.format(cite)
            idx -= 1
            citelist.append(cite)

        cites = '\n'.join(citelist)
        fout.write(cites)
        fout.write('</ol>\n\n')


def main():
    #  parser = argparse.ArgumentParser(
        #  description=__doc__,
        #  formatter_class=argparse.RawDescriptionHelpFormatter)
    #  parser.add_argument('pubmed_ids', type=argparse.FileType('r'))
    #  parser.add_argument('citations', type=argparse.FileType('w'))
    #  args = parser.parse_args()

    PUBMED_LIST = open("_data/pubmed_ids.list")
    pubmed_ids = [p.strip() for p in PUBMED_LIST.readlines()]

    # terrible don't do any of this
    BIORXIV_LIST = open("_data/biorxiv_citations.html")
    biorxiv_citations = []
    for line in BIORXIV_LIST:
        author_title = line.strip()
        journal_date = next(BIORXIV_LIST).strip()
        doi = next(BIORXIV_LIST).strip()
        citation = '<br>\n'.join([author_title, journal_date, doi])
        biorxiv_citations.append(citation)
        try:
            next(BIORXIV_LIST)
        except:
            continue

    CITATION_PAGE = open("publications.md", 'w')

    CITATION_PAGE.write("---\n"
                        "layout: page\n"
                        "title: Publications\n"
                        "permalink: /publications/\n"
                        "---\n")

    citations = scrape_pubmed(pubmed_ids)
    citations = citations + biorxiv_citations
    write_citations(citations, CITATION_PAGE)


if __name__ == '__main__':
    main()
