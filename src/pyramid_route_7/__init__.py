# stdlib
import logging
import re
from typing import Optional
from typing import TYPE_CHECKING

# pypi
from pyramid.exceptions import ConfigurationError

# typing
if TYPE_CHECKING:
    from pyramid.config import Configurator

# ==============================================================================

__VERSION__ = "0.5.2"

# ------------------------------------------------------------------------------

log = logging.getLogger(__name__)

REGEX_route_pattern = re.compile(r"\{(([\w]+)\|([\w]+))\}", re.I)
REGEX_route_kvpattern = re.compile(r"\{(\@([\w]+))\}", re.I)

# ------------------------------------------------------------------------------


def add_route_7_kvpattern(
    config: "Configurator",
    pattern_key: str,
    pattern_regex: str,
):
    r"""
    registers a kvpattern with the configurator.
    a kvpattern is a shortcut pattern for both keys and values.

    :param config: pyramid config
    :type config: `pyramid.config.Configurator` instance
    :param pattern_key: the name of the pattern
    :type pattern_key: str
    :param pattern_regex: the pattern in regex notation
    :type pattern_regex: str
    :returns: None

    it is invoked as such:

        config.add_route_7_kvpattern("year", r"\d\d\d\d")
        config.add_route_7_kvpattern("month", r"\d\d")
        config.add_route_7_kvpattern("day", r"\d\d")
        config.add_route_7("ymd", "/{@year}/{@month}/{@day}")

    this will result in route_7 generating the following route:

        config.add_route("ymd",  r"/{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}")

    it is very useful for matchdicts that you constantly recycle

        config.add_route("user_profile", r"/path/to/user/{user_id:\d\d\d}")
        config.add_route("user_profile-subfolder1", r"/path/to/user/{user_id:\d\d\d}/subfolder-one")
        config.add_route("user_profile-subfolder2", r"/path/to/user/{user_id:\d\d\d}/subfolder-two")

    can now be written as:

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
    registers a pattern with the configurator.
    a pattern is a shortcut pattern for ONLY the values.
    it must be invoked with a key

    :param config: pyramid config
    :type config: `pyramid.config.Configurator` instance
    :param pattern_name: the name of the pattern
    :type pattern_name: str
    :param pattern_regex: the pattern in regex notation
    :type pattern_regex: str
    :returns: None

    it is invoked as such:

        config.add_route_7_pattern("d4", r"\d\d\d\d")
        config.add_route_7_pattern("d2", r"\d\d")
        config.add_route_7("ymd", "/{year|d4}/{month|d2}/{day|d2}")

    note that they syntax for expanding a route_pattern is
        key [pipe] pattern

    this will result in route_7 generating the following route:
        config.add_route("ymd",  r"/{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}")
    """
    if pattern_name in config.registry.route_7["pattern"]:
        raise ConfigurationError("`pattern_name` exists")
    config.registry.route_7["pattern"][pattern_name] = pattern_regex


def add_route_7(
    config: "Configurator",
    name: str,
    pattern: Optional[str] = None,
    jsonify: Optional[bool] = False,
    **kwargs,
) -> None:
    """
    Configuration directive that can be used to register a route
    route_7 allows for a microsyntax in the route declarations.
    after the route declarations are expanded, they are passed onto `add_route`

    if jsonify is true, a second route declaration will be added:
        * The url will be appended with ".json"
        * the route_name will be appented with "|json"

    :param config: pyramid config
    :type config: `pyramid.config.Configurator` instance
    :param name: the name of the route
    :type name: str
    :param pattern: the pattern in regex notation
    :type pattern: str
    :param jsonify: if true, adds a json route and url
    :type jsonify: bool
    :returns: None
    """
    try:
        if pattern:
            _pattern_og = pattern
            _pattern_latest = pattern

            # set dedupes
            _route_patterns = set(REGEX_route_pattern.findall(pattern))
            _route_kvpatterns = set(REGEX_route_kvpattern.findall(pattern))
            if _route_patterns or _route_kvpatterns:
                log.debug("processing %s", pattern)

            for _macro, _key, _p_name in _route_patterns:
                if _p_name not in config.registry.route_7["pattern"]:
                    raise ConfigurationError("missing pattern `%s`" % _p_name)
                _p_value = config.registry.route_7["pattern"][_p_name]
                _pattern_latest = pattern  # stash for logging
                pattern = pattern.replace(_macro, "%s:%s" % (_key, _p_value))
                log.debug("  updating %s > %s", _pattern_latest, pattern)  # updating

            for _macro, _p_name in _route_kvpatterns:
                if _p_name not in config.registry.route_7["kvpattern"]:
                    raise ConfigurationError("missing kvpattern `%s`" % _p_name)
                _p_value = config.registry.route_7["kvpattern"][_p_name]
                _pattern_latest = pattern  # stash for logging
                pattern = pattern.replace(_macro, "%s:%s" % (_p_name, _p_value))
                log.debug("  updating %s > %s", _pattern_latest, pattern)  # updating

            if _pattern_og != pattern:
                log.debug("     final %s > %s", _pattern_og, pattern)  # updating
    except:  # noqa: E722
        raise
    # add the json route first, so the `.json` extension
    # is not consumed by greedy patterns
    if jsonify:
        json_name = "%s|json" % name
        json_pattern = "%s.json" % pattern
        config.add_route(json_name, pattern=json_pattern, **kwargs)
    config.add_route(name, pattern=pattern, **kwargs)


def includeme(config: "Configurator") -> None:
    """Function that gets called when client code calls config.include"""
    config.add_directive("add_route_7", add_route_7)
    config.add_directive("add_route_7_pattern", add_route_7_pattern)
    config.add_directive("add_route_7_kvpattern", add_route_7_kvpattern)
    config.registry.route_7 = {"pattern": {}, "kvpattern": {}}
