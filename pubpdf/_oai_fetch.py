from __future__ import print_function
from __future__ import unicode_literals

import sys
import time

# pyoai
from oaipmh.client import Client
from oaipmh.error import ErrorBase
from oaipmh.metadata import MetadataRegistry

from lxml.etree import tostring


class MetadataSaver(object):
    """A default implementation of a reader that saves the element."""

    def __call__(self, element):
        return element.getchildren()[0]


def get_oai_client(url, prefix):
    registry = MetadataRegistry()
    registry.registerReader(prefix, MetadataSaver())
    client = Client(url, registry)
    return client


def get_oai_record(client, pid, prefix=None):
    if not prefix:
        # Retrieve the prefix provided to `get_oai_client`
        prefix = client._metadata_registry._readers.keys()[0]

    record = None
    attempts = 0
    while not record:
        attempts += 1
        try:
            record = client.getRecord(identifier=pid, metadataPrefix=prefix)
        except ErrorBase:
            raise
        except Exception as e:
            if attempts == 6:
                raise
            print('(connection error: %s)' % e, file=sys.stderr)
            sys.stderr.flush()
            time.sleep(5)
            pass

    return record


def get_oai_document_metadata(client, pid, prefix=None):
    oai_record = get_oai_record(client, pid, prefix=prefix)
    return tostring(oai_record[1])
