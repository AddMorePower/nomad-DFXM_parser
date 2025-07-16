import logging

from nomad.datamodel import EntryArchive

from nomad_dfxm_parser.parsers.parser import NewParser


def test_parse_file():
    parser = NewParser()
    archive = EntryArchive()
    parser.parse('tests/data/example_DFXM_file.h5', archive, logging.getLogger())

    assert archive.data.definition == 'DFXM'
