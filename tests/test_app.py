from __future__ import print_function

"""
IMPORTANT

whitespace in the this file IS SIGNIFICANT AND IMPORTANT.
the test-cases check for specific whitespace
"""

# stdblib
import unittest

# pypi
from pyramid import testing
from webtest import TestApp

# local
# import pyramid_route_7

# ==============================================================================


class PyramidTestApp(unittest.TestCase):
    def setUp(self):
        from .r7testapp import main

        app = main({})
        # create two (cookie) environments for the same app
        self.testapp = TestApp(app)

    def tearDown(self):
        testing.tearDown()

    def test_ymd_kvpattern_good(self):
        res = self.testapp.get("/ymd-kvpattern/2000/02/20", status=200)
        self.assertEqual(res.json["route_name"], "ymd-kvpattern")
        self.assertEqual(res.json["matchdict"]["year"], "2000")
        self.assertEqual(res.json["matchdict"]["day"], "20")
        self.assertEqual(res.json["matchdict"]["month"], "02")

    def test_ymd_kvpattern_bad(self):
        res = self.testapp.get("/ymd-kvpattern/2000/021/20", status=404)
        res = self.testapp.get("/ymd-kvpattern/2000/aa/20", status=404)

    def test_ymd_pattern_good(self):
        res = self.testapp.get("/ymd-pattern/2000/02/20", status=200)
        self.assertEqual(res.json["route_name"], "ymd-pattern")
        self.assertEqual(res.json["matchdict"]["year"], "2000")
        self.assertEqual(res.json["matchdict"]["day"], "20")
        self.assertEqual(res.json["matchdict"]["month"], "02")

    def test_ymd_pattern_bad(self):
        res = self.testapp.get("/ymd-pattern/2000/021/20", status=404)
        res = self.testapp.get("/ymd-pattern/2000/aa/20", status=404)

    def test_user_profile_good(self):
        res = self.testapp.get("/path/to/user/123", status=200)
        self.assertEqual(res.json["route_name"], "user_profile")
        self.assertEqual(res.json["matchdict"]["user_id"], "123")

        res = self.testapp.get("/path/to/user/123/subfolder-one", status=200)
        self.assertEqual(res.json["route_name"], "user_profile-subfolder1")
        self.assertEqual(res.json["matchdict"]["user_id"], "123")

        res = self.testapp.get("/path/to/user/123/subfolder-two", status=200)
        self.assertEqual(res.json["route_name"], "user_profile-subfolder2")
        self.assertEqual(res.json["matchdict"]["user_id"], "123")

    def test_user_profile_bad(self):
        res = self.testapp.get("/path/to/user/1", status=404)
        res = self.testapp.get("/path/to/user/12", status=404)
        res = self.testapp.get("/path/to/user/123/", status=404)
        res = self.testapp.get("/path/to/user/123/1", status=404)
        res = self.testapp.get("/path/to/user/1234", status=404)
        res = self.testapp.get("/path/to/user/a", status=404)
        res = self.testapp.get("/path/to/user/ab", status=404)
        res = self.testapp.get("/path/to/user/abc", status=404)
        res = self.testapp.get("/path/to/user/123/subfolder-1", status=404)

    def test_user_alt(self):
        res = self.testapp.get("/path/to/user-alt/123", status=200)
        self.assertEqual(res.json["route_name"], "user_profile-alt")
        self.assertEqual(res.json["matchdict"]["user_id"], "123")
        self.assertFalse(res.json["jsonify"])

        res = self.testapp.get("/path/to/user-alt/123.json", status=200)
        self.assertEqual(res.json["route_name"], "user_profile-alt|json")
        self.assertEqual(res.json["matchdict"]["user_id"], "123")
        self.assertTrue(res.json["jsonify"])

    def test_items(self):
        res = self.testapp.get("/items", status=200)
        self.assertEqual(res.json["route_name"], "items")
        self.assertFalse(res.json["jsonify"])

        res = self.testapp.get("/items/1", status=200)
        self.assertEqual(res.json["route_name"], "items-paginated")
        self.assertEqual(res.json["matchdict"], {"page": "1"})
        self.assertFalse(res.json["jsonify"])

    def test_items_api(self):
        res = self.testapp.get("/items/api", status=200)
        self.assertEqual(res.json["route_name"], "items_api")
        self.assertFalse(res.json["jsonify"])

        res = self.testapp.get("/items/api.json", status=200)
        self.assertEqual(res.json["route_name"], "items_api|json")
        self.assertTrue(res.json["jsonify"])

        res = self.testapp.get("/items/api/1", status=200)
        self.assertEqual(res.json["route_name"], "items_api-paginated")
        self.assertEqual(res.json["matchdict"], {"page": "1"})
        self.assertFalse(res.json["jsonify"])

        res = self.testapp.get("/items/api/1.json", status=200)
        self.assertEqual(res.json["route_name"], "items_api-paginated|json")
        self.assertEqual(res.json["matchdict"], {"page": "1"})
        self.assertTrue(res.json["jsonify"])

    def test_non_numeric_pages_do_not_match(self) -> None:
        """Reject URLs outside the registered pagination pattern."""
        for path in ("/items/next", "/items/api/next", "/items/api/next.json"):
            with self.subTest(path=path):
                self.testapp.get(path, status=404)

    def test_greedy_filename_route_variants(self) -> None:
        """Dispatch each URL to the most specific generated route."""
        for suffix, route_name, matchdict in (
            ("", "files", {"filename": "docs/manual"}),
            (".json", "files|json", {"filename": "docs/manual"}),
            ("/2", "files-paginated", {"filename": "docs/manual", "page": "2"}),
            ("/2.json", "files-paginated|json", {"filename": "docs/manual", "page": "2"}),
        ):
            with self.subTest(suffix=suffix):
                response = self.testapp.get("/files/docs/manual" + suffix, status=200)
                self.assertEqual(response.json["route_name"], route_name)
                self.assertEqual(response.json["matchdict"], matchdict)
