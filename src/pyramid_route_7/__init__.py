# stdlib
import logging
import re
from typing import Any
from typing import Match
from typing import Optional
from typing import TYPE_CHECKING

# pypi
from pyramid.exceptions import ConfigurationError

# typing
if TYPE_CHECKING:
    from pyramid.config import Configurator

# ==============================================================================

__VERSION__ = "1.0.0"

# ------------------------------------------------------------------------------

log = logging.getLogger(__name__)

_ROUTE_MACRO = re.compile(r"\{(?:(?P<key>\w+)\|(?P<pattern>\w+)|@(?P<kvpattern>\w+))\}", re.I)

# ------------------------------------------------------------------------------


def add_route_7_kvpattern(
    config: "Configurator",
    pattern_key: str,
    pattern_regex: str,
) -> None:
    r"""
    Register a `kvpattern` with the `Configurator`.
    A `kvpattern` is a shortcut pattern for both keys AND values.

    :param config: pyramid config
    :type config: `pyramid.config.Configurator` instance

    :param pattern_key: the name of the pattern
    :type pattern_key: str

    :param pattern_regex: the pattern in regex notation
    :type pattern_regex: str

    :returns: `None`

    It is invoked as such:

        config.add_route_7_kvpattern("year", r"\d\d\d\d")
        config.add_route_7_kvpattern("month", r"\d\d")
        config.add_route_7_kvpattern("day", r"\d\d")
        config.add_route_7("ymd", "/{@year}/{@month}/{@day}")

    The above will result in `pyramid_route_7` generating the following route:

        config.add_route("ymd",  r"/{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}")

    This is useful for `matchdict`s that are re-used across a project.

    The following Pyramid code:

        config.add_route("user_profile", r"/path/to/user/{user_id:\d\d\d}")
        config.add_route("user_profile-subfolder1", r"/path/to/user/{user_id:\d\d\d}/subfolder-one")
        config.add_route("user_profile-subfolder2", r"/path/to/user/{user_id:\d\d\d}/subfolder-two")

    Can now be written as:

        config.add_route_7_kvpattern("user_id", r"\d\d\d")

        config.add_route_7("user_profile", "/path/to/user/{@user_id}")
        config.add_route_7("user_profile-subfolder1", "/path/to/user/{@user_id}/subfolder-one")
        config.add_route_7("user_profile-subfolder2", "/path/to/user/{@user_id}/subfolder-two")
    """
    if pattern_key in config.registry.route_7["kvpattern"]:
        raise ConfigurationError("`pattern_key` exists")
    config.registry.route_7["kvpattern"][pattern_key] = pattern_regex


def add_route_7_pattern(
    config: "Configurator",
    pattern_name: str,
    pattern_regex: str,
) -> None:
    r"""
    Register a `pattern` with the `Configurator`.
    A `pattern` is a shortcut pattern for ONLY the values.
    It MUST be invoked with a key in route declarations.

    :param config: pyramid config
    :type config: `pyramid.config.Configurator` instance

    :param pattern_name: the name of the pattern
    :type pattern_name: str

    :param pattern_regex: the pattern in regex notation
    :type pattern_regex: str

    :returns: `None`

    It is invoked as such:

        config.add_route_7_pattern("d4", r"\d\d\d\d")
        config.add_route_7_pattern("d2", r"\d\d")
        config.add_route_7("ymd", "/{year|d4}/{month|d2}/{day|d2}")

    Note that the syntax for expanding a route_pattern is:

        key [pipe] pattern

    This will result in `pyramid_route_7` generating the following route:
        config.add_route("ymd",  r"/{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}")
    """
    if pattern_name in config.registry.route_7["pattern"]:
        raise ConfigurationError("`pattern_name` exists")
    config.registry.route_7["pattern"][pattern_name] = pattern_regex


def add_route_7(
    config: "Configurator",
    name: str,
    pattern: Optional[str] = None,
    paginate: Optional[bool] = False,
    jsonify: Optional[bool] = False,
    **kwargs: Any,
) -> None:
    r"""
    Configuration directive that can be used to register a route.

    `pyramid_route_7` allows for a microsyntax in the route declarations.

    After the route declarations are expanded, they are passed onto the
    native Pyramid `add_route` command.

    If `jsonify` is `True`, an additional route declaration will be added:
        * The `url` will be appended with ".json"
        * the `route_name` will be appended with "|json"

    In order to defend against greedy patterns, a `jsonify` route will be added
    to the `Configurator` *before* the standard route is added.

    If `paginate` is `True`, an additional route declaration will be added:
        * The `url` will be appended with "/{page:\d+}"
        * the `route_name` will be appended with "-paginated"

    When both options are enabled, the paginated JSON route is registered
    before the unpaginated JSON route. Both precede the non-JSON routes.

    :param config: pyramid config
    :type config: `pyramid.config.Configurator` instance
    :param name: the name of the route
    :type name: str
    :param pattern: the required route pattern
    :type pattern: str
    :param jsonify: if true, adds a json route and url
    :type jsonify: bool
    :param paginate: if true, adds a route and URL with a numeric page segment
    :type paginate: bool
    :returns: None
    """
    if pattern is None:
        raise ConfigurationError("missing route pattern for `%s`" % name)

    def expand_macro(match: Match[str]) -> str:
        """Expand one macro from the original route declaration."""
        kvpattern = match.group("kvpattern")
        if kvpattern is not None:
            kind, key, macro = "kvpattern", kvpattern, kvpattern
        else:
            kind, key, macro = "pattern", match.group("key"), match.group("pattern")
        patterns = config.registry.route_7[kind]
        if macro not in patterns:
            raise ConfigurationError("missing %s `%s`" % (kind, macro))
        return "{%s:%s}" % (key, patterns[macro])

    expanded = _ROUTE_MACRO.sub(expand_macro, pattern)
    if expanded != pattern:
        log.debug("expanded route pattern %s > %s", pattern, expanded)

    if paginate:
        paginated_name = "%s-paginated" % name
        paginated_pattern = r"%s/{page:\d+}" % expanded
        if jsonify:
            config.add_route(
                "%s|json" % paginated_name, pattern="%s.json" % paginated_pattern, **kwargs
            )
    if jsonify:
        config.add_route("%s|json" % name, pattern="%s.json" % expanded, **kwargs)
    if paginate:
        config.add_route(paginated_name, pattern=paginated_pattern, **kwargs)
    config.add_route(name, pattern=expanded, **kwargs)


def includeme(config: "Configurator") -> None:
    """Function that gets called when client code calls config.include"""
    config.add_directive("add_route_7", add_route_7)
    config.add_directive("add_route_7_pattern", add_route_7_pattern)
    config.add_directive("add_route_7_kvpattern", add_route_7_kvpattern)
    config.registry.route_7 = {"pattern": {}, "kvpattern": {}}
