#!/usr/bin/env python

import re
import jonga


if __name__ == "__main__":

    # Construct call tracer object with groups defined by the first
    # part (i.e. before the first '.') of the fully qualified name of
    # the function
    ct = jonga.CallTracer(grpflt='^[^\.]*')

    # Define graph construction option variables
    size='14,12'
    fntsz = 9
    fntfm = 'Vera Sans, DejaVu Sans, Liberation Sans, Arial, Helvetica, sans'

    # Use context manager wrapper of call tracer to trace regex compile
    # function and write a corresponding call graph image.
    with jonga.ContextCallTracer(ct, 'example4.svg', size=size, fntsz=fntsz,
                                fntfm=fntfm):
        rc = re.compile('^[^\.]*.[^\.]*')
