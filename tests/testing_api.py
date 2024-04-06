import unittest
from unittest.mock import patch, MagicMock
# Import your functions
from assignment2.assignment2 import *
import requests


class TestGeospatialFunctions(unittest.TestCase):

    def test_calculate_bearing(self):
        # Example coordinates for the test
        lat1, lon1 = 40.748817, -73.985428  # Empire State Building
        lat2, lon2 = 40.689247, -74.044502  # Statue of Liberty

        expected_bearing = 165  # Expected bearing, replace with correct value
        result = calculate_bearing(lat1, lon1, lat2, lon2)
        self.assertAlmostEqual(result, expected_bearing,
                               places=1, msg="Bearing calculation is incorrect.")

    def test_get_cardinal_direction(self):
        bearing = 70  # Example bearing
        expected_direction = 'NE'  # Expected direction
        result = get_cardinal_direction(bearing)
        self.assertEqual(result, expected_direction,
                         "Cardinal direction is incorrect.")

    def test_get_side_of_town_and_coords(self, mock_geocode):
        mock_geocode.return_value = [
            {'geometry': {'location': {'lat': 40.748817, 'lng': -73.985428}}}]
        expected_result = ('NE', (40.748817, -73.985428))  # Expected result

        result = get_side_of_town_and_coords(
            "Empire State Building, NY", MagicMock())
        self.assertEqual(result, expected_result,
                         "Side of town and coordinates are incorrect.")


# Add more test cases for other functions

if __name__ == '__main__':
    unittest.main()
