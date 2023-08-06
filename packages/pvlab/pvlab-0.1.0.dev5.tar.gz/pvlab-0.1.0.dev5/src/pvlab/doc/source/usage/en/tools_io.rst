==============
I/O Management
==============

Provide tools for data input/output.

dicts from Source Files
^^^^^^^^^^^^^^^^^^^^^^^

.. py:module:: pvlab.io.dictmaker

Generate python dictionaries from multiple files and data types.

New functions are intended to read files of parameters and convert each
data file into a python dictionary. Different type of parameters should be
located in different files, for better performance.

It contains the following functions:

Function get_dict
"""""""""""""""""

.. py:function:: pvlab.io.dictmaker.get_dict(file: TypeVar('File', str, io.StringIO), dtype: str, sep: str = ':', isStringIO: bool = False) -> dict:

   Generate a python dictionary from a file of parameters.

   Function ``get_dict`` reads a file that contains parameters in the form
   *[name]: [value]* (or in other general form *[name][sep] [value]*, if
   specified).
   It requires specifying the type of data contained in the file, admitting
   types ``int``, ``float``, ``tuple`` or ``str`` (unknown data types are
   admitted, but they will be parsed as *raw* strings).
   Originally designed for data-acquisition purposes. It also admits
   ``io.StringIO`` objects instead, if argument ``isStringIO`` is specified
   as ``True`` (e.g. useful for exemplification purposes).

**Example 1**: ``int`` type arguments:

.. code-block:: python

   data = "readings:21\nminG:600\nrefG:1000"
   settings = get_dict(io.StringIO(data), dtype='int', isStringIO=True)
   # ... argument ``io.StringIO(data)`` can be replaced by a file name.
   settings
   {'readings': 21, 'minG': 600, 'refG': 1000}


**Example 2**: ``str`` type arguments:

.. code-block:: python

   data = "man.:'manufacturer'\nmod.:'model'\nsn.:'seriesnr'"
   mydict = get_dict(io.StringIO(data), dtype='str', isStringIO=True)
   mydict
   {'man.': 'manufacturer', 'mod.': 'model', 'sn.': 'seriesnr'}


Function get_dicts_list
"""""""""""""""""""""""

.. py:function:: pvlab.io.dictmaker.get_dicts_list(filelist: Iterable[str],  dtypelist: Iterable[str], isStringIO: Iterable[bool] = False, sep: str = ':') -> dict:

   Generate a list of dicts from a list of parameter files or ``io.StringIO``
   objects.

   It uses the previous function ``get_dict`` recursively, from correlative
   values of ``filelist`` and ``dtypelist`` arguments.


**Example 3**: source objects containing both ``float`` and ``str`` arguments.

.. code-block:: python

   floatdata = "maxdev:0.02\noffsetthreeshold:2.0"
   filters = io.StringIO(floatdata)  # StringIO_1 (or filename_1)
   strdata = "mode_refpyr:'voltage'\nmode_dut:'currentloop'"
   calmode = io.StringIO(strdata)  # StringIO_2 (or filename_2)
   isstringio = ['True', 'True']  # io.StringIO objects? (defaults False)
   caliblist = get_dicts_list([filters, calmode], ['float', 'str'], isStringIO=isstringio)  # it returns a list of python dicts.
   caliblist[0]  # ...data from StringIO_1 (or filename_1)
   {'maxdev': 0.02, 'offsetthreeshold': 2.0}
   caliblist[1]  # ... data from StringIO_2 (or filename_2)
   {'mode_refpyr': 'voltage', 'mode_dut': 'currentloop'}
   