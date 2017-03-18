import pytest

import collections

import re
import jonga


class TestSet01(object):

    def test_01(self):
        ct = jonga.CallTracer(dstflt='^(re.|sre_)', grpflt='^[^\.]*')
        ct.start()
        rec = re.compile('^[^\.]*.[^\.]*')
        ct.stop()
        g = ct.graph()
        assert(g is not None)
        s = str(ct)
        assert(s != '')
