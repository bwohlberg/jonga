#!/usr/bin/env python

import re
import jonga


if __name__ == "__main__":

    # Construct call tracer object with groups defined by the first
    # part (i.e. before the first '.') of the fully qualified name of
    # the function
    ct = jonga.CallTracer(grpflt='^[^\.]*')
    # Start call tracing
    ct.start()

    # Call regex compile function
    rc = re.compile('^[^\.]*.[^\.]*')

    # Stop tracing
    ct.stop()
    # Define font family specification string
    fntfm = 'Vera Sans, DejaVu Sans, Liberation Sans, Arial, Helvetica, sans'
    # Write graph in dot format
    ct.graph('example3.dot', size='14,12', fntsz=9, fntfm=fntfm)
    # Write graph in SVG format
    ct.graph('example3.svg', size='14,12', fntsz=9, fntfm=fntfm)
