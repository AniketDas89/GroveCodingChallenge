import unittest
import find_store


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_get_local_coordinates_zipcode(self):
        coordinates = find_store.get_local_coordinates('94545')
        self.assertEqual(coordinates, (37.6362740630492, -122.102387330493))

    def test_get_local_coordinates_address(self):
        coordinates = find_store.get_local_coordinates('One Infinite Loop Cupertino, CA')
        self.assertEqual(coordinates, (37.3317585, -122.0320474))

    def test_get_local_coordinates_invalid(self):
        coordinates = find_store.get_local_coordinates('Sea of Tranquility, Moon')
        self.assertIsNone(coordinates)

    def test_get_closest_store(self):
        expected = {'Store Name': 'Cupertino',
                    'Store Location': 'NWC Stevens Creek & Bandley Dr',
                    'Address': '20745 Stevens Creek Blvd',
                    'City': 'Cupertino',
                    'State': 'CA',
                    'Zip Code': '95014-2123',
                    'Latitude': '37.3241877',
                    'Longitude': '-122.0361026',
                    'County': 'Santa Clara County',}
        store, distance = find_store.find_closest_store((37.3317585, -122.0320474))
        self.assertDictEqual(store, expected)
        self.assertAlmostEqual(distance, 0.9138752225311382, delta=0.01)

    def test_calculate_great_circle_far(self):
        expected = 13239.0950
        actual = find_store.calculate_great_circle_km((37.135, -120.44262), (-43.113, 142.335))
        self.assertAlmostEqual(expected, actual, delta=0.01)

    def test_calculate_great_circle_near(self):
        expected = 0.9138752225311382
        actual = find_store.calculate_great_circle_km((37.3317585, -122.0320474), (37.3241877, -122.0361026))
        self.assertAlmostEqual(actual, expected, delta=0.01)

    def test_get_radial_coordinates(self):
        expected_phi = 1.57
        expected_lambda = .785398
        actual_phi, actual_lambda = find_store.get_radial_coordinates((90, 45))
        self.assertAlmostEqual(expected_phi, actual_phi, delta=0.01)
        self.assertAlmostEqual(expected_lambda, actual_lambda, delta=0.01)


if __name__ == '__main__':
    unittest.main()
