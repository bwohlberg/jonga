import os
import tempfile
import re
import pytest
import jonga


class TestSet01(object):

    def test_01(self):
        ct = jonga.CallTracer(dstmodflt='^(re.|sre_)', grpflt=r'^[^\.]*')
        ct.start()
        rec = re.compile(r'^[^\.]*.[^\.]*')
        ct.stop()
        assert ct.graph() is not None
        assert str(ct) != ''
        ct.reset()
        assert str(ct) == ''


    def test_02(self):
        with jonga.ContextCallTracer(
            jonga.CallTracer(grpflt=r'^[^\.]*')) as cct:
            rec = re.compile(r'^[^\.]*.[^\.]*')
        ct = cct.calltracer()
        assert str(ct) != ''
        ct.reset()
        assert str(ct) == ''


    def test_03(self):
        ct = jonga.CallTracer(grpflt=r'^[^\.]*')
        fd, pth = tempfile.mkstemp(suffix='.svg')
        os.close(fd)
        with jonga.ContextCallTracer(ct, pth):
            rec = re.compile(r'^[^\.]*.[^\.]*')
        assert os.path.getsize(pth) > 0
        os.remove(pth)


    def test_04(self):
        ct = jonga.CallTracer(grpflt=r'^[^\.]*')
        fd, pth = tempfile.mkstemp(suffix='.svg')
        os.close(fd)
        with jonga.ContextCallTracer(ct, pth, rmsz=True):
            rec = re.compile(r'^[^\.]*.[^\.]*')
        assert os.path.getsize(pth) > 0
        os.remove(pth)
