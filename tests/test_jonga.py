import pytest

import collections

import re
import jonga


class TestSet01(object):

    def test_01(self):
        ct = jonga.CallTracer(grpflt='^[^\.]*')
        ct.start()
        rec = re.compile('^[^\.]*.[^\.]*')
        ct.stop()
        g = ct.graph()
        s = str(ct)
