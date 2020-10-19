Route 7
=======

.. image:: https://github.com/jvanasco/pyramid_route_7/workflows/Python%20package/badge.svg
        :alt: Build Status

`pyramid_route_7` extends pyramid's routing to have provide a macro syntax that can be easier to maintain on larger projects.

It works through a ridiculously simple mechanism -- when calling `add_route_7` instead of `add_route`, the package expands the macros in the route declaration, then immediately calls pyramid's own `add_route`.

Usage
=====

There are two main patterns supported by `pyramid_route_7`:

route_kvpattern
---------------

A `kvpattern` ties a key to a pattern.
The macro is invoked by the key, and generates both the key and pattern.

Here is a canonical example:

.. code-block:: python

    config.add_route_7_kvpattern('year', '\d\d\d\d')
    config.add_route_7_kvpattern('month', '\d\d')
    config.add_route_7_kvpattern('day', '\d\d')
    config.add_route_7('ymd', '/{@year}/{@month}/{@day}')

this will result in route_7 generating the following route:

.. code-block:: python

    config.add_route('ymd',  /{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}')

note that they syntax for expanding a route_kvpattern is

.. code-block:: shell

	@ key
    [at-sign] key


route_pattern
-------------
A `pattern` represents a reusable regex.
The macro is invoked by the pattern_name, and generates only the pattern regex.

Here is a canonical example:

.. code-block:: python

    config.add_route_7_pattern('d4', '\d\d\d\d')
    config.add_route_7_pattern('d2', '\d\d')
    config.add_route_7('ymd', '/{year|d4}/{month|d2}/{day|d2}')

this will result in route_7 generating the following route:

.. code-block:: python

    config.add_route_7('ymd',  '/{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}')

note that they syntax for expanding a route_pattern is

.. code-block:: shell

    key [pipe] pattern

while the syntax for a route is

.. code-block:: shell

    key [colon] regex


FAQ:
====

Q: Why package?
---------------

In larger applications (dozens of routes), it's not uncommon to see lots of patterns re-used.

This package was designed to consolidate the patterns in one place so they can be centrally managed and upgraded over time.


Q: Why the name "route_7"?
--------------------------
A: Two reasons:
* It makes it trivial to implement on existing projects by replacing `add_route` with `add_route_7`, and vice-versa
* "The Lurid Traversal of Route 7" by Hoover, might... just might... be the best album on Dischord records. (http://www.dischord.com/release/089/lurid-traversal-of-rte-7)


Q: Any integration tips?
------------------------

By default the package will emit logging activity on how it upgrades routes (expands macros) to the default logger.  If you have any troubles, that will help!

A very fast way to integrate routes is just using find & replace.

Step 1 - Define Macros
______________________

Before you declare your first route like this:

.. code-block:: python

    config.add_route("main", "/")
    config.add_route("foo", "/foo")
    config.add_route("foo_paginated", "/foo/{page:\d+}")

You should include the package and define some macros

.. code-block:: python

    # incude pyramid_route_7 and define our routes/macros
    config.include("pyramid_route_7")
    config.add_route_7_kvpattern('page', '\d+')

	 # okay, go!
	 config.add_route("main", "/")
	 config.add_route("foo", "/foo")
	 config.add_route("foo_paginated", "/foo/{page:\d+}")

Step 2 - Just use find & replace in a couple of passes
______________________________________________________

First, replace `config.add_route` with `config.add_route_7`:

.. code-block:: python

	# incude pyramid_route_7 and define our routes/macros
	config.include("pyramid_route_7")
	config.add_route_7_kvpattern('page', '\d+')

    # okay, go!
    # config.add_route("main", "/")
 	config.add_route_7("main", "/")
    # config.add_route("foo", "/foo")
    config.add_route_7("foo", "/foo")
    # config.add_route("foo_paginated", "/foo/{page:\d+}")
    config.add_route_7("foo_paginated", "/foo/{page:\d+}")

Then find/replace your macros:

.. code-block:: python

	# incude pyramid_route_7 and define our routes/macros
	config.include("pyramid_route_7")
	config.add_route_7_kvpattern('page', '\d+')

	# okay, go!
    config.add_route_7("main", "/")
    config.add_route_7("foo", "/foo")
    # config.add_route_7("foo_paginated", "/foo/{page:\d+}")
    config.add_route_7("foo_paginated", "/foo/{@page}")

Because `add_route_7` simply expands registered macros and passes the result to Pyramid's own `add_route`,
you can just run it on every declared route.  The performance hit is only at startup
and is incredibly minimal (it's really just a regex).
