from __future__ import print_function

import pyramid_route_7

# stdblib
import unittest

# pypi
from pyramid import testing
from pyramid.urldispatch import Route
from pyramid.interfaces import IRoutesMapper


# ==============================================================================


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.config = config = testing.setUp()
        config.include("pyramid_route_7")
        config.add_route_7_pattern("d4", r"\d\d\d\d")
        config.add_route_7_pattern("d2", r"\d\d")
        config.add_route_7_kvpattern("year", r"\d\d\d\d")
        config.add_route_7_kvpattern("month", r"\d\d")
        config.add_route_7_kvpattern("day", r"\d\d")
        config.add_route_7_kvpattern("user_id", r"\d\d\d")
        # define routes: TOTAL-5
        config.add_route_7("ymd-pattern", "/ymd-pattern/{year|d4}/{month|d2}/{day|d2}")
        config.add_route_7("ymd-kvpattern", "/ymd-kvpattern/{@year}/{@month}/{@day}")
        config.add_route_7("user_profile", "/path/to/user/{@user_id}")
        config.add_route_7(
            "user_profile-subfolder1", "/path/to/user/{@user_id}/subfolder-one"
        )
        config.add_route_7(
            "user_profile-subfolder2", "/path/to/user/{@user_id}/subfolder-two"
        )
        # END define routes
        self.context = testing.DummyResource()
        self.request = testing.DummyRequest()

        # https://github.com/Pylons/pyramid/blob/master/tests/test_config/test_routes.py
        #    def _assertRoute(self, config, name, path, num_predicates=0)
        self.mapper = mapper = self.config.registry.getUtility(IRoutesMapper)
        self.routes = routes = mapper.get_routes()
        self.routes_dict = {r.name: r.pattern for r in routes}

    def tearDown(self):
        testing.tearDown()

    def test_setup(self):
        # if setup failed, the following would have raised exceptions
        #   in `_TestHarness.setUp` :
        #   * `config.add_route_7_pattern`
        #   * `config.add_route_7_kvpattern`
        #   * `config.add_route_7`
        # just ensure we added 5 routes
        self.assertEqual(5, len(self.routes))

    def test_pattern(self):
        self.assertIn("ymd-pattern", self.routes_dict)
        _route_pattern = self.routes_dict["ymd-pattern"]
        self.assertEqual(
            _route_pattern, r"/ymd-pattern/{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}"
        )

    def test_kvpattern(self):
        self.assertIn("ymd-kvpattern", self.routes_dict)
        _route_pattern = self.routes_dict["ymd-kvpattern"]
        self.assertEqual(
            _route_pattern, r"/ymd-kvpattern/{year:\d\d\d\d}/{month:\d\d}/{day:\d\d}"
        )

        self.assertIn("user_profile", self.routes_dict)
        _route_pattern = self.routes_dict["user_profile"]
        self.assertEqual(_route_pattern, r"/path/to/user/{user_id:\d\d\d}")

        self.assertIn("user_profile-subfolder1", self.routes_dict)
        _route_pattern = self.routes_dict["user_profile-subfolder1"]
        self.assertEqual(
            _route_pattern, r"/path/to/user/{user_id:\d\d\d}/subfolder-one"
        )

        self.assertIn("user_profile-subfolder2", self.routes_dict)
        _route_pattern = self.routes_dict["user_profile-subfolder2"]
        self.assertEqual(
            _route_pattern, r"/path/to/user/{user_id:\d\d\d}/subfolder-two"
        )
