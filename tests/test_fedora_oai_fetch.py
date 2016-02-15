import unittest

from oaipmh.error import IdDoesNotExistError

from pubpdf._fedora_oai_fetch import get_oai_client
from pubpdf._fedora_oai_fetch import get_oai_document_metadata


class OAITest(unittest.TestCase):

    def test_une_valid(self):
        url = 'https://e-publications.une.edu.au/oaiprovider/'
        pid = 'une:18767'
        client = get_oai_client(url, prefix='mods')
        xml = get_oai_document_metadata(client, pid)
        assert xml.tag.startswith('{http://www.loc.gov/mods/')
        assert xml.tag.endswith('}mods')

    def test_une_invalid(self):
        url = 'https://e-publications.une.edu.au/oaiprovider/'
        pid = 'une:-1'
        client = get_oai_client(url, prefix='mods')
        self.assertRaises(IdDoesNotExistError,
                          get_oai_document_metadata, client, pid)
