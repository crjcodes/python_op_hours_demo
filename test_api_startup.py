import unittest
import api_startup
import manager_operating_hours


class StartupTests(unittest.TestCase):
    def test_should_throw_exception_when_no_manager(self):
        test_manager = manager_operating_hours.Manager()
        self.assertRaises(ValueError, api_startup.perform_startup_steps, None, "")

    def test_should_throw_exception_when_no_input_data_file(self):
        test_manager = manager_operating_hours.Manager()
        self.assertRaises(ValueError, api_startup.perform_startup_steps, test_manager, "")

    def test_should_have_converted_data_when_nominal_input_data(self):
        test_manager = manager_operating_hours.Manager()
        api_startup.perform_startup_steps(test_manager, "test_input_data.csv")

        self.assertNotEqual("", test_manager.Accessor.Data)
        self.assertIsNotNone(test_manager.Accessor.Data)


if __name__ == '__main__':
    unittest.main()
