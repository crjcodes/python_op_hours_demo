import sys, logging
import unittest
from dateutil import parser
import json
import manager_operating_hours, accessor_operating_hours

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

class OperationHoursManagerTests(unittest.TestCase):
    def test_matches_ShouldReturnRestaurants_WhenValidDateTime(self):
        test_manager = manager_operating_hours.Manager()
        test_manager.ingest_new_data_source("test_input_data.csv")

        test_accessor = test_manager.Accessor
        test_timestamp = parser.parse("21:30").time()
        restaurants = test_accessor.matches('Sat', test_timestamp)
        self.assertTrue(len(restaurants) == 3)

    def test_matches_ShouldReturnRestaurants_WhenValidDateTimeEvening(self):
        test_manager = manager_operating_hours.Manager()
        test_manager.ingest_new_data_source("test_input_data.csv")
        test_accessor = test_manager.Accessor
        test_timestamp = parser.parse("7pm").time()
        restaurants = test_accessor.matches('Sat', test_timestamp)
        self.assertEqual(4, len(restaurants))