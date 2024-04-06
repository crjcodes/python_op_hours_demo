from dateutil import parser


class Accessor:

    def __init__(self):
        self.Data = {}

    def store(self, bulk_data):
        self.Data = bulk_data

    def matches(self, day_of_week, time):
        matching_restaurant_names = []

        # TODO: FUTURE: validate inputs
        # TODO: FUTURE: opportunity to refactor cleaner, more performant

        for establishment in self.Data.keys():
            dow_list = self.Data[establishment].keys()
            for dow in dow_list:
                if day_of_week != dow:
                    continue

                op_hours = self.Data[establishment][dow]
                start_time = parser.parse(op_hours.start).time()
                end_time = parser.parse(op_hours.end).time()
                if start_time <= time < end_time:
                    matching_restaurant_names.append(establishment)

        return matching_restaurant_names
