import string
from datetime import datetime
import engine_convert
import accessor_operating_hours


# import operating_hours_accessor

class Manager:

    def __init__(self):
        self.Accessor = accessor_operating_hours.Accessor()

    def list_operating_restaurants(self, date_time_text):
        if date_time_text is None:
            raise ValueError("Datetime not given")

        dow = ""
        try:
            datestamp = datetime.strptime(date_time_text, '%m/%d/%y %H:%M:%S')
            dow = datestamp.weekday()
            timestamp = datestamp.time()
            restaurants = self.Accessor.matches(dow, timestamp)
            return restaurants

        except:
            raise ValueError("Given date is invalid")

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
