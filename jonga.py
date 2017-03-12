#-*- coding: utf-8 -*-
# Copyright (C) 2017 by Brendt Wohlberg <brendt@ieee.org>
# All rights reserved. GPLv2+ License.

"""Call tracing for class method inheritance documentation"""

import re
import sys
if sys.version_info < (3,3):
    raise RuntimeError('Module jonga requires Python version 3.3 or greater')
import os
import gc
import inspect
import colorsys

import pygraphviz as pgv


__version__ = '0.0.1'
__author__ = """Brendt Wohlberg <brendt@ieee.org>"""


def current_function(frame):
    """
    Get reference to currently running function from inspect/trace stack frame.

    Parameters
    ----------
    frame : stack frame
      Stack frame obtained via trace or inspect

    Returns
    -------
    fnc : function reference
      Currently running function
    """

    if frame is None:
        return None

    code = frame.f_code
    # Attempting to extract the function reference for these calls appears
    # to be problematic
    if code.co_name == '__del__' or code.co_name == '_remove' or \
       code.co_name == '_removeHandlerRef':
        return None

    # Solution follows that suggested at http://stackoverflow.com/a/37099372
    lst = [referer for referer in gc.get_referrers(code)
           if getattr(referer, "__code__", None) is code and
           inspect.getclosurevars(referer).nonlocals.items() <=
           frame.f_locals.items()]
    if len(lst) > 0:
        return lst[0]
    else:
        return None



def function_fqname(fnc):
    """
    Get fully qualified name of a function

    Parameters
    ----------
    fnc : function reference
      A function reference

    Returns
    -------
    fqn : string
      The fully qualified name the function
    """

    if fnc is None:
        return ''
    else:
        return fnc.__module__ + '.' + fnc.__qualname__



def current_module_name(frame):
    """
    Get name of module of currently running function from inspect/trace
    stack frame.

    Parameters
    ----------
    frame : stack frame
      Stack frame obtained via trace or inspect

    Returns
    -------
    modname : string
      Currently running function module name
    """

    if frame is None:
        return None

    if hasattr(frame.f_globals, '__name__'):
        return frame.f_globals['__name__']
    else:
        mod = inspect.getmodule(frame)
        if mod is None:
            return ''
        else:
            return mod.__name__



class CallTracer(object):
    """
    Manage construction of a call graph for methods within a class hierarchy
    """

    def __init__(self, srcflt=None, dstflt=None, fnmsub=None, grpflt=None,
                 lnksub=None):
        """Initialise a CallTracer object.

        Parameters
        ----------
        srcflt : None or regex string, optional (default None)
          A regex for call filtering based on calling function fqname. A
          function call is only recorded if the regex matches the name of
          the calling function. If None, filtering is disabled.
        dstflt : None or regex string, optional (default None)
          A regex for call filtering based on caller function fqname. A
          function call is only recorded if the regex matches the name of
          the called function. If None, filtering is disabled.
        fnmsub : None or tuple of two regex strings, optional (default None)
          A tuple of match and replace regex strings for computing graph node
          names from function qnames. If None, node names are function qnames.
        grpflt : None or regex string, optional (default None)
          A regex string for extracting part of the function fqname as a
          group name. If None, groups are not defined.
        lnksub : None or tuple of two regex strings, optional (default None)
          A tuple of match and replace regex strings for computing node href
          attributes from node names. If None, href attributes are not defined.
        """

        # Regex for caller function module filtering
        if srcflt is None:
            srcflt = '.*'
        # Regex for called function module filtering
        if dstflt is None:
            dstflt = srcflt
        # Compiled regex for caller function module filtering
        self.srcflt = re.compile(srcflt)
        # Compiled regex for called function module filtering
        self.dstflt = re.compile(dstflt)
        # Regex pair for function name replacment
        self.fnmsub = fnmsub
        # Regex for constructing function grouping string
        if grpflt is None:
            self.grpflt = None
        else:
            self.grpflt = re.compile(grpflt)
        # Regex for link target construction
        self.lnksub = lnksub

        # Dict associating function name with list containing counts
        # of occurrences in caller and called roles
        self.fncts = {}
        # Dict associating tuple of (caller,called) function names
        # with counts of such calls
        self.calls = {}
        # Dict associating group match string with corresponding functions
        self.group = {}



    def _trace(self, frame, event, arg):
        """
        Build a record of called functions using the trace mechanism
        """

        # Return if this is not a function call
        if event != 'call':
            return

        # Filter calling and called functions by module names
        src_mod = current_module_name(frame.f_back)
        dst_mod = current_module_name(frame)
        if not self.srcflt.match(src_mod):
            return
        if not self.dstflt.match(dst_mod):
            return

        # Get calling and called functions
        src_func = current_function(frame.f_back)
        dst_func = current_function(frame)

        # Get calling and called function full names
        src_name = function_fqname(src_func)
        dst_name = function_fqname(dst_func)

        # Modify full function names if necessary
        if self.fnmsub is not None:
            src_name = re.sub(self.fnmsub[0], self.fnmsub[1], src_name)
            dst_name = re.sub(self.fnmsub[0], self.fnmsub[1], dst_name)

        # Update calling function count
        if src_func is not None:
            if src_name in self.fncts:
                self.fncts[src_name][0] += 1
            else:
                self.fncts[src_name] = [1,0]

        # Update called function count
        if dst_func is not None and src_func is not None:
            if dst_name in self.fncts:
                self.fncts[dst_name][1] += 1
            else:
                self.fncts[dst_name] = [0,1]

        # Update caller/calling pair count
        if dst_func is not None and src_func is not None:
            key = (src_name, dst_name)
            if key in self.calls:
                self.calls[key] += 1
            else:
                self.calls[key] = 1



    def start(self):
        """Start tracing"""

        sys.settrace(self._trace)



    def stop(self):
        """Stop tracing"""

        # Stop tracing
        sys.settrace(None)

        # Build group structure if group filter is defined
        if self.grpflt is not None:
            # Iterate over graph nodes (functions)
            for k in self.fncts:
                # Construct group identity string
                m = self.grpflt.search(k)
                # If group identity string found, append current node
                # to that group
                if m is not None:
                    ms = m.group(0)
                    if ms in self.group:
                        self.group[ms].append(k)
                    else:
                        self.group[ms] = [k,]




    @staticmethod
    def _clrgen(n, h0, hr):
        """Default colour generating function

        Parameters
        ----------

        n : int
          Number of colours to generate
        h0 : float
          Initial H value in HSV colour specification
        hr : float
          Size of H value range to use for colour generation
          (final H value is h0 + hr)

        Returns
        -------
        clst : list of strings
          List of HSV format colour specification strings
        """

        n0 = n if n == 1 else n-1
        clst = ['%f,%f,%f' % (h0 + hr*hi/n0, 0.35, 0.85) for
                hi in range(n)]
        return clst



    def graph(self, fnm=None, size=None, fntsz=None, fntfm=None, clrgen=None,
              prog='dot'):
        """
        Construct call graph

        Parameters
        ----------
        fnm : None or string, optional (default None)
          Filename of graph file to be written. File type is determined by
          the file extentions (e.g. dot for 'graph.dot' and SVG for
          'graph.svg'). If None, a file is not written.
        size : string or None, optional (default None)
          Graph image size specification string.
        fntsz : int or None, optional (default None)
          Font size for text.
        fntnm : string or None, optional (default None)
          Font family specification string.
        clrgen : function or None, optional (default None)
          Function to call to generate the group colours. This function
          should take an integer specifying the number of groups as an
          argument and return a list of graphviz-compatible colour
          specification strings.
        prog : string, optional (default 'dot')
          Name of graphviz layout program to use.

        Returns
        -------
        pgr : pygraphviz.AGraph
          Call graph of traced function calls
        """

        # Default colour generation function
        if clrgen is None:
            clrgen = lambda n : self._clrgen(n, 0.330, 0.825)

        # Generate color list
        clrlst = clrgen(len(self.group))

        # Initialise a pygraphviz graph
        g = pgv.AGraph(strict=False, directed=True, landscape=False,
                       rankdir='LR', newrank=True, fontsize=fntsz,
                       fontname=fntfm, size=size, ratio='compress',
                       color='black', bgcolor='#ffffff00')
        # Set graph attributes
        g.node_attr.update(penwidth=0.25, shape='box', style='rounded,filled')

        # Iterate over functions adding them as graph nodes
        for k in self.fncts:
            g.add_node(k, fontsize=fntsz, fontname=fntfm)
            # If lnksub regex pair is provided, compute an href link
            # target from the node name and add it as an attribute to
            # the node
            if self.lnksub is not None:
                lnktgt = re.sub(self.lnksub[0], self.lnksub[1], k)
                g.get_node(k).attr.update(href=lnktgt, target="_top")
            # If function has no calls to it, set its rank to "source"
            if self.fncts[k][1] == 0:
                g.get_node(k).attr.update(rank='source')

        # If groups defined, construct a subgraph for each and add the
        # nodes in each group to the corresponding subgraph
        if self.group:
            fngrpnm = {}
            # Iterate over group number/group name pairs
            for k in zip(range(len(self.group)), sorted(self.group)):
                g.add_subgraph(self.group[k[1]], name='cluster_' + k[1],
                               label=k[1], penwidth=2, style='dotted',
                               pencolor=clrlst[k[0]])
                # Iterate over nodes in current group
                for l in self.group[k[1]]:
                    # Create record of function group number
                    fngrpnm[l] = k[0]
                    # Set common group colour for current node
                    g.get_node(l).attr.update(fillcolor=clrlst[k[0]])

        # Iterate over function calls, adding each as an edge
        for k in self.calls:
            # If groups defined, set edge colour according to group of
            # calling function, otherwise set a standard colour
            if self.group:
                g.add_edge(k[0], k[1], penwidth=2, color=clrlst[fngrpnm[k[0]]])
            else:
                g.add_edge(k[0], k[1], color='grey')

        # Call layout program
        g.layout(prog=prog)

        # Write graph file if filename provided
        if fnm is not None:
            if os.path.splitext(fnm)[1] == 'dot':
                g.write(fnm)
            else:
                g.draw(fnm)

        # Return graph object
        return g



    def __str__(self):
        """Get string representation"""

        s = ''
        for k in self.fncts:
            s += '%-40s   %2d  %2d\n' % (k, self.fncts[k][0], self.fncts[k][1])
        for k in self.calls:
            s += '%-35s  ->  %-35s  %2d\n' % (k[0], k[1], self.calls[k])
        for k in self.group:
            s += '%s\n    ' % k
            for l in self.group[k]:
                s += '%s  ' % l
            s += '\n'
        return s
