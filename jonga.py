# -*- coding: utf-8 -*-
# Copyright (C) 2017-2018,2024 by Brendt Wohlberg <brendt@ieee.org>
# All rights reserved. GPLv2+ License.

"""Call tracing for class method inheritance documentation"""

import os
import gc
import inspect
import re
import sys
if sys.version_info < (3, 3):
    raise RuntimeError('Module jonga requires Python version 3.3 or greater')

import pygraphviz as pgv


__version__ = '0.0.5b1'
__author__ = """Brendt Wohlberg <brendt@ieee.org>"""


__modulename__ = sys.modules[__name__].__name__


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

    try:
        # Solution follows suggestion at http://stackoverflow.com/a/37099372
        lst = [referer for referer in gc.get_referrers(code)
               if getattr(referer, "__code__", None) is code and
               inspect.getclosurevars(referer).nonlocals.items() <=
               frame.f_locals.items()]
        if lst:
            return lst[0]
        else:
            return None
    except ValueError:
        # inspect.getclosurevars can fail with ValueError: Cell is empty
        return None



def function_qname(fnc):
    """
    Get qualified name of a function (the fully qualified name without
    the module prefix).

    Parameters
    ----------
    fnc : function reference
      A function reference

    Returns
    -------
    fqn : string
      The qualified name the function
    """

    if fnc is None:
        return ''
    else:
        return fnc.__qualname__



def function_fqname(fnc):
    """
    Get fully qualified name of a function.

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
    Manage construction of a call graph for methods within a class hierarchy.
    """

    def __init__(self, srcmodflt=None, dstmodflt=None, srcqnmflt=None,
                 dstqnmflt=None, fnmsub=None, grpflt=None, lnksub=None):
        """
        Parameters
        ----------
        srcmodflt : None or regex string, optional (default None)
          A regex for call filtering based on calling function module. A
          function call is only recorded if the regex matches the name of
          the calling function module. If None, filtering is disabled.
        dstmodflt : None or regex string, optional (default None)
          A regex for call filtering based on caller function. A
          function call is only recorded if the regex matches the name of
          the called function module. If None, filtering is disabled.
        srcqnmflt : None or regex string, optional (default None)
          A regex for call filtering based on calling function qname. A
          function call is only recorded if the regex matches the name of
          the calling function. If None, filtering is disabled.
        dstqnmflt : None or regex string, optional (default None)
          A regex for call filtering based on caller function qname. A
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
        if srcmodflt is None:
            srcmodflt = '.*'
        # Regex for called function module filtering
        if dstmodflt is None:
            dstmodflt = srcmodflt
        # Compiled regex for caller function module filtering
        self.srcmodflt = re.compile(srcmodflt)
        # Compiled regex for called function module filtering
        self.dstmodflt = re.compile(dstmodflt)

        # Regex for caller function qname filtering
        if srcqnmflt is None:
            srcqnmflt = '.*'
        # Regex for called function qname filtering
        if dstqnmflt is None:
            dstqnmflt = srcqnmflt
        # Compiled regex for caller function qname filtering
        self.srcqnmflt = re.compile(srcqnmflt)
        # Compiled regex for called function qname filtering
        self.dstqnmflt = re.compile(dstqnmflt)

        # Regex pair for function name replacement
        self.fnmsub = fnmsub
        # Regex for constructing function grouping string
        if grpflt is None:
            self.grpflt = None
        else:
            self.grpflt = re.compile(grpflt)
        # Regex for link target construction
        self.lnksub = lnksub

        # Initialise dicts for recording call information
        self.reset()


    def reset(self):
        """
        Reset record of called functions, deleting all accumulated call
        information.
        """

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
        Build a record of called functions using the trace mechanism.
        """

        # Return if this is not a function call
        if event != 'call':
            return

        # Filter calling and called functions by module names
        src_mod = current_module_name(frame.f_back)
        dst_mod = current_module_name(frame)

        # Avoid tracing the tracer (specifically, call from
        # ContextCallTracer.__exit__ to CallTracer.stop)
        if src_mod == __modulename__ or dst_mod == __modulename__:
            return

        # Apply source and destination module filters
        if not self.srcmodflt.match(src_mod):
            return
        if not self.dstmodflt.match(dst_mod):
            return

        # Get calling and called functions
        src_func = current_function(frame.f_back)
        dst_func = current_function(frame)

        # Filter calling and called functions by qnames
        if not self.srcqnmflt.match(function_qname(src_func)):
            return
        if not self.dstqnmflt.match(function_qname(dst_func)):
            return

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
                self.fncts[src_name] = [1, 0]

        # Update called function count
        if dst_func is not None and src_func is not None:
            if dst_name in self.fncts:
                self.fncts[dst_name][1] += 1
            else:
                self.fncts[dst_name] = [0, 1]

        # Update caller/calling pair count
        if dst_func is not None and src_func is not None:
            key = (src_name, dst_name)
            if key in self.calls:
                self.calls[key] += 1
            else:
                self.calls[key] = 1


    def start(self):
        """Start tracing."""

        sys.settrace(self._trace)


    def stop(self):
        """Stop tracing."""

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
                        self.group[ms] = [k, ]



    @staticmethod
    def _clrgen(n, h0, hr):
        """Default colour generating function.

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
              rmsz=False, prog='dot'):
        """
        Construct call graph.

        Parameters
        ----------
        fnm : None or string, optional (default None)
          Filename of graph file to be written. File type is determined
          by the file extensions (e.g. dot for 'graph.dot' and SVG for
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
        rmsz : bool, optional (default False)
          If True, remove the width and height specifications from an
          SVG format output file so that the size scales properly when
          viewed in a web browser
        prog : string, optional (default 'dot')
          Name of graphviz layout program to use.

        Returns
        -------
        pgr : pygraphviz.AGraph
          Call graph of traced function calls
        """

        # Default colour generation function
        if clrgen is None:
            clrgen = lambda n: self._clrgen(n, 0.330, 0.825)

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
            ext = os.path.splitext(fnm)[1]
            if ext == '.dot':
                g.write(fnm)
            else:
                if ext == '.svg' and rmsz:
                    img = g.draw(format='svg').decode('utf-8')
                    cp = re.compile(r'\n<svg width=\"[^\"]*\" '
                                    'height=\"[^\"]*\"')
                    img = cp.sub(r'\n<svg', img, count=1)
                    with open(fnm, 'w') as fd:
                        fd.write(img)
                else:
                    g.draw(fnm)

        # Return graph object
        return g


    def __str__(self):
        """Get string representation."""

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




class ContextCallTracer(object):
    """
    A wrapper class for :class:`CallTracer` that enables its use as a
    context manager. At the end of the context a call graph image is
    generated and written to a path specified in the initialiser.
    """

    def __init__(self, ct, pth=None, **kwargs):
        """
        Parameters
        ----------
        ct : class:`CallTracer` object
          Specify the call tracer object to be used as a context manager.
        pth : string or None, optional (default None)
          Specify the path of the graph image file to be written by
          :meth:`CallTracer.graph` at the end of the context. A graph is
          not generated if it is ``None``.
        **kwargs
          Keyword arguments for :meth:`CallTracer.graph`
        """

        self.ct = ct
        self.pth = pth
        self.kwargs = kwargs


    def __enter__(self):
        """
        Reset and start call tracer and return this ContextCallTracer
        instance.
        """

        self.ct.reset()
        self.ct.start()
        return self


    def __exit__(self, extype, value, traceback):
        """
        Stop the call tracer and return True if no exception was raised
        within the 'with' block, otherwise return False.
        """

        self.ct.stop()
        if self.pth is not None:
            self.ct.graph(self.pth, **self.kwargs)
        if extype:
            return False
        else:
            return True


    def calltracer(self):
        """
        Return the call tracer object associated with this ContextCallTracer
        instance.
        """

        return self.ct
