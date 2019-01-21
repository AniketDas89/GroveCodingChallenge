import unittest
import find_store


class MyTestCase(unittest.TestCase):

    def test_get_local_coordinates_zipcode(self):
        coordinates = find_store.get_local_coordinates('94545')
        self.assertEqual(coordinates, (37.633392, -122.106689))

    def test_get_local_coordinates_address(self):
        coordinates = find_store.get_local_coordinates('One Infinite Loop Cupertino, CA')
        self.assertEqual(coordinates, (37.3321, -122.03074))

    def test_get_closest_store(self):
        expected = {'Store Name': 'Cupertino',
                    'Store Location': 'NWC Stevens Creek & Bandley Dr',
                    'Address': '20745 Stevens Creek Blvd',
                    'City': 'Cupertino',
                    'State': 'CA',
                    'Zip Code': '95014-2123',
                    'Latitude': 37.3241877,
                    'Longitude': -122.0361026,
                    'County': 'Santa Clara County'}
        actual = find_store.find_closest_store((37.3321, -122.03074))
        self.assertDictEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
