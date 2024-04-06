import unittest
import manager_operating_hours


class OperationHoursManagerTests(unittest.TestCase):
    def test_list_operating_restaurants_ShouldReturnRestaurants_WhenValidDateTime(self):
        test_manager = manager_operating_hours.Manager()
        test_manager.ingest_new_data_source("test_input_data.csv")
        restaurants = test_manager.list_operating_restaurants("2024-01-01 7:00pm")
        self.assertEqual(3,len(restaurants))

    def test_list_operating_restaurants_ShouldReturnRestaurants_WhenValidDateTime24(self):
        test_manager = manager_operating_hours.Manager()
        test_manager.ingest_new_data_source("test_input_data.csv")
        restaurants = test_manager.list_operating_restaurants("2024-01-01 19:00")
        self.assertEqual(3,len(restaurants))

    def test_list_operating_restaurants_ShouldReturnNone_WhenValidDateTime(self):
        test_manager = manager_operating_hours.Manager()
        test_manager.ingest_new_data_source("test_input_data.csv")
        restaurants = test_manager.list_operating_restaurants("2024-01-01 05:00")
        self.assertEqual(0,len(restaurants))

    def test_list_operating_restaurants_ShouldReturnNone_WhenValidDateTimeClosing(self):
        test_manager = manager_operating_hours.Manager()
        test_manager.ingest_new_data_source("test_input_data.csv")
        restaurants = test_manager.list_operating_restaurants("2024-04-05 21:50")
        self.assertTrue("The Cowfish Sushi Burger Bar" in restaurants)
        self.assertTrue("Garland" in restaurants)
        self.assertTrue("Crawford and Son" in restaurants)

