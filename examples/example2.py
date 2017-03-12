#!/usr/bin/env python

import xmpl
import jonga


if __name__ == "__main__":

    # Construct call tracer object set to filter out calls of
    # functions/methods within module xmpl, with the effective
    # function name constructed by replacing the initial 'xmpl.' with
    # the empty string, and with groups defined by
    # the first part (i.e. before the first '.') of the fully
    # qualified name of the function *after* the string substitution
    ct = jonga.CallTracer(srcflt='^xmpl', fnmsub=('^xmpl.', ''),
                          grpflt='^[^\.]*')
    # Construct object from example class
    c = xmpl.C()
    # Start call tracing
    ct.start()

    # Call 'run' method of example class
    c.run()

    # Stop tracing
    ct.stop()

    # Write graph in dot format
    ct.graph('example2a.dot')
    # Write graph in SVG format
    ct.graph('example2a.svg')

    # Define custom colour generation function by calling default
    # colour generation function with different parameters
    clrgen = lambda n : jonga.CallTracer._clrgen(n, 0.330, 0.330)
    # Write graph in dot format with custom colours
    ct.graph('example2b.dot', clrgen=clrgen)
    # Write graph in SVG format with custom colours
    ct.graph('example2b.svg', clrgen=clrgen)
