#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright © 2017 Matthew Stone <mstone5@mgh.harvard.edu>
# Distributed under terms of the MIT license.

"""

"""

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

    # get article data
    citation = article['MedlineCitation']['Article']

    def _parse_author(author):
        name = author['LastName'] + ' ' + author['Initials']
        if name == "Stone MR":
            name = "**{0}**".format(name)
        return name

    authors = [_parse_author(author) for author in citation['AuthorList']]
    authors = ', '.join(authors)

    title = citation['ArticleTitle'].replace(u'\xa0', ' ').rstrip('.')
    journal = citation['Journal']['ISOAbbreviation'].replace('.', '')

    date = parse_pubmed_date(article)
    issue = parse_pubmed_issue(citation)

    # note: trailing doublespace necessary for line break in markdown
    citation = ("{authors}. {title}.  \n"
                "_{journal}_. {date};{issue}. doi: {doi}.").format(**locals())

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
