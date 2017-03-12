#!/usr/bin/env python

import xmpl
import jonga


if __name__ == "__main__":

    # Construct call tracer object set to filter out calls of
    # functions/methods within module xmpl
    ct = jonga.CallTracer(srcflt='^xmpl')
    # Start call tracing
    ct.start()

    # Construct object from example class
    c = xmpl.C()

    # Stop tracing
    ct.stop()
    # Write graph in dot format
    ct.graph('example1a.dot')
    # Write graph in SVG format
    ct.graph('example1a.svg')



    # Construct call tracer object set to filter out calls of
    # functions/methods within module xmpl and with the displayed
    # function name constructed by replacing the initial 'xmpl.' with
    # the empty string
    ct = jonga.CallTracer(srcflt='^xmpl', fnmsub=('^xmpl.', ''))
    # Start call tracing
    ct.start()

    # Construct object from example class
    c = xmpl.C()

    # Stop tracing
    ct.stop()
    # Write graph in dot format
    ct.graph('example1b.dot')
    # Write graph in SVG format
    ct.graph('example1b.svg')



    # Construct call tracer object set to filter out calls of
    # functions/methods within module xmpl and with groups defined by
    # the first part (i.e. before the first '.') of the fully
    # qualified name of the function
    ct = jonga.CallTracer(srcflt='^xmpl', grpflt='^[^\.]*')
    # Start call tracing
    ct.start()

    # Construct object from example class
    c = xmpl.C()

    # Stop tracing
    ct.stop()
    # Write graph in dot format
    ct.graph('example1c.dot')
    # Write graph in SVG format
    ct.graph('example1c.svg')

