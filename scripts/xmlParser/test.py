import filecmp
import pytest

#Compare two xml file. If true, pytest is defined by "PASS"
def test_FileComparing():
    compression = filecmp.cmp('./scripts/xmlParser/Father.xml', './scripts/xmlParser/Son.xml')
    assert(compression)