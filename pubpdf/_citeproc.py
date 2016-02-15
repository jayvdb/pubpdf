from __future__ import print_function
from __future__ import unicode_literals

import codecs

from citeproc import Citation
from citeproc import CitationItem
from citeproc import CitationStylesBibliography
from citeproc import CitationStylesStyle
from citeproc import formatter
from citeproc.source.bibtex import BibTeX


def convert_bibtex_to_csl_data(bibs):
    # TODO: use a StringIO to avoid writing to file

    # FIXME: proper unique temporary filenames
    filename = '/tmp/bib.tex'
    with codecs.open(filename, 'w', 'utf8') as f:
        f.write(bibs)

    return BibTeX(filename, encoding='utf8')


def _cite_warn(citation_item):
    print("WARNING: Reference with key '{}' not found in the bibliography."
          .format(citation_item.key))


def generate_html(bib_csl_data, style_name='harvard1'):
    assert bib_csl_data
    bib_source = bib_csl_data
    bib_style = CitationStylesStyle(style_name, validate=False)

    bibliography = CitationStylesBibliography(
        bib_style, bib_source, formatter.html)

    bib_cites = [Citation([CitationItem(item)]) for item in bib_source]

    # print(bib_cites[0]['cites'][0]['key'])

    for item in bib_cites:
        bibliography.register(item)

    # FIXME: Is this needed?
    for item in bib_cites:
        bibliography.cite(item, _cite_warn)

    out = ''
    bibliography.sort()
    for item in bibliography.bibliography():
        line = '<p>' + ''.join(item) + '</p>\n'

        out += line

    return out
