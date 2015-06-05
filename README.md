# Route 7

`Route 7` extends pyramid's routing to have provide a macro syntax that can be easier to maintain on larger proejcts.

It works through a ridiculously simple mechanism -- when calling `add_route_7` instead of `add_route`, the package exapnds the macros in the route declaration, then immediately calls pyramid's own `add_route`.

# Usage

There are two main patterns supported by route_7

## route_kvpattern

A `kvpattern` ties a key to a pattern.
The macro is invoked by the key, and generates both the key and pattern.

Here is a canonical example:

    config.add_route_7_kvpattern('year', '\d\d\d\d')
    config.add_route_7_kvpattern('month', '\d\d')
    config.add_route_7_kvpattern('day', '\d\d')
    config.add_route_7('ymd', '/{@year}/{@month}/{@day}')

this will result in route_7 generating the following route:

    config.add_route('ymd',  /{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}')

note that they syntax for expanding a route_kvpattern is

    [at-sign] key


## route_pattern
A `pattern` represents a reusable regex.
The macro is invoked by the pattern_name, and generates only the pattern regex.

Here is a canonical example:
    config.add_route_7_pattern('d4', '\d\d\d\d')
    config.add_route_7_pattern('d2', '\d\d')
    config.add_route_7('ymd', '/{year|d4}/{month|d2}/{day|d2}')

this will result in route_7 generating the following route:
    config.add_route_7('ymd',  '/{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}')

note that they syntax for expanding a route_pattern is

    key [pipe] pattern

while the syntax for a route is

    key [colon] regex


# FAQ:

## Q: Why package?

In larger applications (dozens of routes), it's not uncommon to see lots of patterns re-used.

This package was designed to consolidate the patterns so they can be centrally managed and upgraded over time.


## Q: Why the name "route_7"?
A: Two reasons:
* It makes it trivial to implement on existing projects by replacing `add_route` with `add_route_7`, and vice-versa
* "The Lurid Traversal of Route 7", by Hoover, might just be the best album on Dischord records. (http://www.dischord.com/release/089/lurid-traversal-of-rte-7)
