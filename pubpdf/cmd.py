from __future__ import print_function
from __future__ import unicode_literals

import codecs
import itertools
import os.path
import re

from collections import defaultdict, OrderedDict

import citeproc.frontend

from bibutils.wrapper import convert

from oaipmh.error import ErrorBase

from pubpdf.config import get_options

from pubpdf._citeproc import convert_bibtex_to_csl_data, generate_html
from pubpdf._oai_fetch import get_oai_client, get_oai_document_metadata
from pubpdf._mods import create_mods_collection

from weasyprint import HTML


def convert_mods_to_bib(mods):
    # Fix unrecognised genre 'journal article'
    mods = mods.replace('genre>journal article<', 'genre>article-journal<')

    # This would workaround book chapter being misunderstood
    # mods = mods.replace('>book chapter<', '>instruction<')

    mods = re.sub(
        r'<mods:namePart type="given">([^< ]*) ([^<]*)</mods:namePart>',
        r'<mods:namePart type="given">\1</mods:namePart>\n<mods:namePart type="given">\2</mods:namePart>',
        mods)

    # workaround bug in bibutils
    # https://github.com/jayvdb/patches/blob/master/bibutils-une.diff
    mods = mods.replace('mods:original', 'mods:series')

    bibs = convert(mods, 'xml', 'bib', encoding='utf8')

    # workaround bibutils emitting issue & number,
    # and citeproc-py only parsing number.
    if 'issue=' in bibs:
        bibs = re.sub('number=.*', '', bibs)
        bibs = bibs.replace('issue=', 'number=')

    return bibs.replace('\nand ', ' and ')


def fetch_csl_data(api, prefix, pids):
    """Return mods collection containing records of each pid."""
    client = get_oai_client(api, prefix)
    pubs = []

    for pid in pids:
        pubs.append(get_oai_document_metadata(client, pid))

    mods = create_mods_collection(pubs)

    return mods


def _load_mods_files(filenames):
    """Return mods collection from file."""
    pubs = []
    for filename in filenames:
        with codecs.open(filename, 'r', 'utf8') as f:
            pubs.append(f.read())

    mods = create_mods_collection(pubs)
    return mods


def split_pubs_by_type(pubs, type_map=None):
    batches = defaultdict(dict)

    for key, item in pubs.items():
        print(item.type, key)
        if type_map and item.type in type_map:
            pub_type = item.type
        else:
            pub_type = 'misc'

        batches[pub_type][key] = item

    return batches


def generate_html_by_type(pubs, type_map, csl_style):
    html = ''
    batches = split_pubs_by_type(pubs, type_map)
    for pub_type, label in type_map.items():
        if pub_type in batches:
            html += '\n\n<h2>' + label + '</h2>\n\n'
            html += generate_html(batches[pub_type], csl_style)

    return html


def generate_pdf(filename, html):
    HTML(string=html).write_pdf(filename)


_type_labels = OrderedDict({
    'book': 'Books',
    'chapter': 'Chapters',
    'article-journal': 'Articles',
    'article': 'Articles',
    'report': 'Papers',
    'conference publication': 'Conference Publication',
    'misc': 'Others',
})


def _generate(options):
    bibs = None
    mods = None
    if os.path.exists(options.pids[0]):
        filename = options.pids[0]
        if filename.endswith('.bib'):
            with codecs.open(filename, 'r', 'utf8') as f:
                bibs = f.read()
        else:
            mods = _load_mods_files(options.pids)
    else:
        mods = fetch_csl_data(options.oai_api, options.oai_format, options.pids)

    if mods:
        with codecs.open(options.output_file + '.mods', 'w', 'utf8') as output_file:
            output_file.write(mods)

    if not bibs:
        bibs = convert_mods_to_bib(mods)

        with codecs.open(options.output_file + '.bib', 'w', 'utf8') as output_file:
            output_file.write(bibs)

    pubs = convert_bibtex_to_csl_data(bibs)

    html = options.html_preamble

    if options.group_by_type:
        html += generate_html_by_type(pubs, _type_labels, options.csl_style)
    else:
        html += generate_html(pubs, options.csl_style)

    html += '\n  </body>\n</html>\n'

    with codecs.open(options.output_file + '.html', 'w', 'utf8') as output_file:
        output_file.write(html)

    generate_pdf(options.output_file, html)


def main():
    options = get_options()

    if options.csl_style_dir:
        citeproc.frontend.STYLES_PATH = options.csl_style_dir

    if options.check_oai_repo:
        assert options.oai_format == 'mods'
        assert options.oai_api
        assert len(options.pids) <= 2

        start = 1
        end = None
        if options.pids:
            _, start = options.pids[0].split(':', 1)
            start = int(start)
            if len(options.pids) > 1:
                _, end = options.pids[1].split(':', 1)
                end = int(end)

        for i in itertools.count(start):
            if end and i > end:
                break

            options.pids = [options.oai_identifier_prefix + ':' + str(i)]
            try:
                _generate(options)
            except ErrorBase as e:
                print('error %s : %s' % (options.pids[0], e))

        print('OK')
        return

    assert options.pids
    _generate(options)
