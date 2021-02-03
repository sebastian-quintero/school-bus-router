import unittest

from models.location import Location


class TestsLocation(unittest.TestCase):
    """Tests for the Location class"""

    def test_post_init_geohash(self):
        """
        Assert the actions taken after the class is instantiated and a geohash
        is defined
        """

        geohash = 'd2g6g6'
        location = Location(
            lat=4.718400,
            lng=-74.027692,
            geohash=geohash
        )
        self.assertEqual(
            location.geohash, geohash,
            msg='The geohash for the Location is encoded incorrectly.'
        )

    def test_post_init_no_geohash(self):
        """
        Assert the actions taken after the class is instantiated and no
        geohash is defined
        """

        location = Location(
            lat=4.718400,
            lng=-74.027692
        )
        self.assertEqual(
            location.geohash, 'd2g6g6ywtv80',
            msg='The geohash for the Location is encoded incorrectly.'
        )

    def test_extract_geohash(self):
        """Assert the geohash extraction is done correctly"""

        location = Location(
            lat=4.718400,
            lng=-74.027692
        )
        self.assertEqual(
            location.extract_geohash(6),
            'd2g6g6',
            msg='Geohash of precision 6 is extracted incorrectly.'
        )
        self.assertEqual(
            location.extract_geohash(8),
            'd2g6g6yw',
            msg='Geohash of precision 8 is extracted incorrectly.'
        )
