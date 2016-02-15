from __future__ import unicode_literals
from __future__ import unicode_literals


def create_mods_collection(pubs):
    """
    Return a <modsCollection> XML document.

    @rtype: unicode
    """
    s = '<?xml version="1.0" encoding="UTF-8"?>\n'
    s += '<modsCollection xmlns="http://www.loc.gov/mods/v3">\n'
    for pub in pubs:
        s += pub + '\n'
    s += '\n</modsCollection>\n'
    return s
