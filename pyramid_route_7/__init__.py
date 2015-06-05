import logging
log = logging.getLogger(__name__)

from pyramid.exceptions import ConfigurationError

import re


# ==============================================================================


REGEX_route_pattern = re.compile('\{(([\w]+)\|([\w]+))\}', re.I)
REGEX_route_kvpattern = re.compile('\{(\@([\w]+))\}', re.I)


# ==============================================================================


def add_route_7_kvpattern(
    config,
    pattern_key,
    pattern_regex
):
    """registers a kvpattern with the configurator.
        a kvpattern is a shortcut pattern for both keys and values.

        it is invoked as such:

            config.add_route_7_kvpattern('year', '\d\d\d\d')
            config.add_route_7_kvpattern('month', '\d\d')
            config.add_route_7_kvpattern('day', '\d\d')
            config.add_route('ymd', '/{@year}/{@month}/{@day}')

        this will result in route_seven generating the following route:
            config.add_route('ymd',  /{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}')

        it is very useful for matchdicts that you constantly recycle

            config.add_route('user_profile', '/path/to/user/{user_id:\d\d\d}')
            config.add_route('user_profile-subfolder1', '/path/to/user/{user_id:\d\d\d}/subfolder-one')
            config.add_route('user_profile-subfolder2', '/path/to/user/{user_id:\d\d\d}/subfolder-two')

        can now be:

            config.add_route_7_kvpattern('user_id', '\d\d\d')
            config.add_route('user_profile', '/path/to/user/{@user_id}')
            config.add_route('user_profile-subfolder1', '/path/to/user/{@user_id}/subfolder-one')
            config.add_route('user_profile-subfolder2', '/path/to/user/{@user_id}/subfolder-two')
    """
    if pattern_key in config.registry.route_7['kvpattern']:
        raise ConfigurationError('`pattern_key` exists')
    config.registry.route_7['kvpattern'][pattern_key] = pattern_regex


def add_route_7_pattern(
    config,
    pattern_name,
    pattern_regex
):
    """registers a pattern with the configurator.
        a pattern is a shortcut pattern for ONLY the values.
        it must be invoked with a key
        it is invoked as such:

            config.add_route_7_pattern('d4', '\d\d\d\d')
            config.add_route_7_pattern('d2', '\d\d')
            config.add_route('ymd', '/{year|d4}/{month|d2}/{day|d2}')

        note that they syntax for expanding a route_pattern is
            key [pipe] pattern

        this will result in route_seven generating the following route:
            config.add_route('ymd',  /{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}')
    """
    if pattern_name in config.registry.route_7['pattern']:
        raise ConfigurationError('`pattern_name` exists')
    config.registry.route_7['pattern'][pattern_name] = pattern_regex


def add_route_7(
    config,
    name,
    pattern=None,
    **kwargs
):
    """Configuration directive that can be used to register a route
        route_seven allows for a microsyntax in the route declarations.
        after the route declarations are expanded, they are passed onto `add_route`
    """
    try:
        if pattern:
            _pattern_og = pattern
            _pattern_latest = pattern

            # set dedupes
            _route_patterns = set(REGEX_route_pattern.findall(pattern))
            _route_kvpatterns = set(REGEX_route_kvpattern.findall(pattern))
            if (_route_patterns or _route_kvpatterns):
                log.debug("processing %s", pattern)

            for (_macro, _key, _p_name) in _route_patterns:
                if _p_name not in config.registry.route_7['pattern']:
                    raise ConfigurationError('missing pattern `%s`' % _p_name)
                _p_value = config.registry.route_7['pattern'][_p_name]
                _pattern_latest = pattern  # stash for logging
                pattern = pattern.replace(_macro, '%s:%s' % (_key, _p_value))
                log.debug("  updating %s > %s", _pattern_latest, pattern)  # updating

            for (_macro, _p_name) in _route_kvpatterns:
                if _p_name not in config.registry.route_7['kvpattern']:
                    raise ConfigurationError('missing kvpattern `%s`' % _p_name)
                _p_value = config.registry.route_7['kvpattern'][_p_name]
                _pattern_latest = pattern  # stash for logging
                pattern = pattern.replace(_macro, '%s:%s' % (_p_name, _p_value))
                log.debug("  updating %s > %s", _pattern_latest, pattern)  # updating

            if _pattern_og != pattern:
                log.debug("     final %s > %s", _pattern_og, pattern)  # updating
    except:
        raise
    config.add_route(name, pattern=pattern, **kwargs)


def includeme(config):
    """Function that gets called when client code calls config.include"""
    config.add_directive('add_route_7', add_route_7)
    config.add_directive('add_route_7_pattern', add_route_7_pattern)
    config.add_directive('add_route_7_kvpattern', add_route_7_kvpattern)
    config.registry.route_7 = {'pattern': {},
                               'kvpattern': {},
                               }
