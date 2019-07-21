import filecmp
import pytest

#Compare two xml file. If true, pytest is defined by "PASS"
def test_array():
    compression = filecmp.cmp('Father.xml', 'Son.xml')
    assert(compression)