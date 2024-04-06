import unittest
import engine_convert


class EngineConvertTests(unittest.TestCase):
    valid_lines = [
        "The Cowfish Sushi Burger Bar,Mon-Sun 11:00 am - 10 pm",
        "Morgan St Food Hall,Mon-Sun 11 am - 9:30 pm",
        "Beasley's Chicken + Honey,\"Mon-Fri, Sat 11 am - 12 pm  / Sun 11 am - 10 pm\"",
        "Garland,Tues-Fri, Sun 11:30 am - 10 pm  / Sat 5:30 pm - 11 pm",
        "Crawford and Son,Mon-Sun 11:30 am - 10 pm"
    ]

    # region parse_last_time_text

    # TODO: use input test data into one test, not two sets in sequence
    def test_parse_last_time_text_ShouldReturnNone_WhenInvalidInput(self):
        modifiedTestData, timeText = engine_convert.parse_last_time_text("")
        self.assertIsNone(timeText)
        self.assertEqual("", modifiedTestData)

        modifiedTestData, timeText = engine_convert.parse_last_time_text("blah blah")
        self.assertIsNone(timeText)
        self.assertEqual("blah blah", modifiedTestData)

    def test_parse_last_time_text_ShouldReturnTimeAsText_WhenGivenSampleData(self):
        testData = "Mon-Thu, Sun 11 am - 10 pm"
        modifiedTestData, timeText = engine_convert.parse_last_time_text(testData)
        self.assertIsNotNone(timeText)
        self.assertEqual("10pm", timeText)

    def test_parse_last_time_text_ShouldReturnEndAndOpenTimeAsText_WhenGivenSampleData(self):
        """
        More of a "sequence" test than a unit test
        """

        testData = "Mon-Thu, Sun 11 am - 10 pm"

        modifiedTestData, timeText = engine_convert.parse_last_time_text(testData)

        self.assertIsNotNone(timeText)
        self.assertEqual("10pm", timeText)
        self.assertEqual("Mon-Thu, Sun 11 am", modifiedTestData)

        modifiedTestData, timeText = engine_convert.parse_last_time_text(modifiedTestData)
        self.assertIsNotNone(timeText)
        self.assertEqual("11am", timeText)
        self.assertEqual("Mon-Thu, Sun ", modifiedTestData)

    # endregion

    # region parse_dow_text
    def test_parse_dow_text_ShouldReturnExpectedListofDaysOfWeek_WhenGivenBadData(self):
        testData = "Mon-Thu, TBD "
        result = engine_convert.parse_dow_text(testData)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual("Mon", result[0])
        self.assertEqual("Tue", result[1])
        self.assertEqual("Wed", result[2])
        self.assertEqual("Thu", result[3])

        testData = "TBD-Thu, Sun"
        result = engine_convert.parse_dow_text(testData)

        self.assertEqual("Sun", result[0])

        testData = "Mon-TBD, Sun"
        result = engine_convert.parse_dow_text(testData)

        self.assertEqual("Sun", result[0])

    def test_parse_dow_text_ShouldReturnExpectedListofDaysOfWeek_WhenGivenSampleData(self):
        testData = "Mon-Thu, Sun "
        result = engine_convert.parse_dow_text(testData)

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertEqual("Mon", result[0])
        self.assertEqual("Tue", result[1])
        self.assertEqual("Wed", result[2])
        self.assertEqual("Thu", result[3])
        self.assertEqual("Sun", result[4])

    # endregion

    # region parse_op_hours
    def test_parse_op_hours_ShouldReturnNone_WhenInvalidInput(self):

        self.assertIsNone(engine_convert.parse_op_hours(""))
        self.assertIsNone(engine_convert.parse_op_hours(None))
        return

    def test_parse_op_hours_ShouldReturnDict_WhenValidParsedTime(self):
        result = engine_convert.parse_op_hours("\"Mon-Fri, Sat 11 am - 12 pm  / Sun 11 am - 10 pm\"")
        self.assertTrue("Mon" in result.keys())
        self.assertTrue("Thu" in result.keys())
        self.assertTrue("Sat" in result.keys())
        self.assertTrue("Sun" in result.keys())
        self.assertEqual("11:00", result["Mon"].start)
        self.assertEqual("11:00", result["Sun"].start)
        self.assertEqual("22:00", result["Sun"].end)

    def test_parse_op_hours_ShouldReturnExpectedListofDaysOfWeek_WhenGivenComplexData(self):
        test_data = "\"Tues-Fri, Sun 11:30 am - 10 pm  / Sat 5:30 pm - 11 pm\""
        result = engine_convert.parse_op_hours(test_data)

        self.assertIsNotNone(result)
        self.assertFalse("Mon" in result.keys())
        self.assertTrue("Tue" in result.keys())
        self.assertTrue("Fri" in result.keys())
        self.assertTrue("Sat" in result.keys())
        self.assertTrue("Sun" in result.keys())
        self.assertEqual("11:30", result["Sun"].start)
        self.assertEqual("23:00", result["Sat"].end)

    # endregion

    # region parse_time
    def test_parse_time_ShouldReturnFormattedTime_WhenGivenARangeofFormattedTimestamp(self):
        testData = ["11am", "11:30 am", "1 pm", "9:30 pm", "5:30pm", " 12 pm  ", "11:53 pm"]
        expectedResult = ["11:00", "11:30", "13:00", "21:30", "17:30", "12:00", "23:53"]

        i = 0
        for t in testData:
            result = engine_convert.parse_time(t)
            self.assertEqual(result, expectedResult[i])
            i = i + 1

    # endregion

    # region split_line
    def test_split_line_ShouldReturnCorrectSplit_WhenGivenQuotedField(self):
        result = engine_convert.split_line(self.valid_lines[2])
        self.assertIsNotNone(result)
        self.assertEqual(2, len(result))
# endregion
