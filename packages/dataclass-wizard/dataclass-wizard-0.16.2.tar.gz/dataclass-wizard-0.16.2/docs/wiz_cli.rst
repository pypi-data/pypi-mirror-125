.. highlight:: shell

The CLI Tool
============

The ``wiz`` command provides a companion CLI tool for the Dataclass Wizard,
which further simplifies interaction with the Python ``dataclasses`` module.

Getting help::

    $ wiz -h
    usage: wiz [-h] [-V] {gen-schema,gs} ...

    A companion CLI tool for the Dataclass Wizard, which simplifies interaction with the Python `dataclasses` module.

    positional arguments:
      {gen-schema,gs}  Supported sub-commands
        gen-schema (gs)
                       Generates a Python dataclass schema, given a JSON input.

    optional arguments:
      -h, --help       show this help message and exit
      -V, --version    Display the version of this tool.

Checking the version of the CLI tool should display the currently installed
version of the ``dataclass-wizard`` library::

    $ wiz -V

To get help on a subcommand, simply use ``wiz <subcommand> -h``. For example::

    $ wiz gs -h

JSON To Dataclass Generation Tool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The subcommand ``gen-schema`` (aliased to ``gs``) provides a JSON to Python
schema generation tool. This utility takes a JSON file or string as an input,
and outputs the corresponding dataclass schema. The main purpose is to easily
create dataclasses that can be used with API output, without resorting to
``dict``'s or ``NamedTuple``'s.

This scheme generation tool is inspired by the following projects:

-  https://github.com/mischareitsma/json2dataclass
-  https://russbiggs.github.io/json2dataclass
-  https://github.com/mholt/json-to-go
-  https://github.com/bermi/Python-Inflector

.. note:: A few things to consider:

  - The script sometimes has to make some assumptions, so give the output a once-over.
  - In an array of objects (i.e. dictionaries), all key names and type definitions get merged into a single
    model ``dataclass``, as the objects are considered homogenous in this case.
  - Deeply nested lists within objects (e.g. *list* -> *dict* -> *list*) should
    similarly merge all list elements with the other lists under that key in
    each sibling `dict` object.
  - The output is properly formatted, including additional spacing where needed.
    Please consider `opening an issue`_ if there are any potential improvements
    to be made.

Example usage::

    echo '{
        "name": "Yavin IV",
        "rotation_period": "24",
        "orbital_period": "4818",
        "diameter": "10200",
        "climate": "temperate, tropical",
        "gravity": "1 standard",
        "terrain": "jungle, rainforests",
        "surface_water": "8",
        "population": "1000",
        "residents": [],
        "films": [
            "https://swapi.co/api/films/1/"
        ],
        "created": "2014-12-10T11:37:19.144000Z",
        "edited": "2014-12-20T20:58:18.421000Z",
        "url": "https://swapi.co/api/planets/3/"
    }' | wiz gs

Generates the following Python code::

    from dataclasses import dataclass
    from datetime import datetime
    from typing import List, Union


    @dataclass
    class Data:
        """
        Data dataclass

        """
        name: str
        rotation_period: Union[int, str]
        orbital_period: Union[int, str]
        diameter: Union[int, str]
        climate: str
        gravity: str
        terrain: str
        surface_water: Union[int, str]
        population: Union[int, str]
        residents: List
        films: List[str]
        created: datetime
        edited: datetime
        url: str


Note: to write the output to a Python file instead of displaying the
output in the terminal, pass the name of the output file. If the file
has no extension, a default ``.py`` extension will be added.

For example::

    # Note: the following command writes to a new file 'out.py'

    echo '<json string>' | wiz gs - out


.. _`opening an issue`: https://github.com/rnag/dataclass-wizard/issues
