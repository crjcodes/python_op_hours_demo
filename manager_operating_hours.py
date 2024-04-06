from dateutil import parser
import engine_convert
import accessor_operating_hours


class Manager:

    def __init__(self):
        self.Accessor = accessor_operating_hours.Accessor()

    def list_operating_restaurants(self, date_time_text):
        if date_time_text is None:
            raise ValueError("Datetime not given")

        try:
            datestamp = parser.parse(date_time_text)
            dow = datestamp.strftime('%a')
            timestamp = datestamp.time()
            restaurants = self.Accessor.matches(dow, timestamp)
            return restaurants

        except Exception as err:
            raise ValueError(f"Given date is invalid, {err}")

    def ingest_new_data_source(self, filename):
        """
        This approach will NOT work for larger input
        One alternative approach is to have a background or separate
        process ingest the csv in chunks at a time and store in a database
        Then, here, the accessor could access the database instead of
        an internal json structure held in memory
        """
        self.Accessor.store(engine_convert.ConvertFrom(filename))
        return
