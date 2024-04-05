class Accessor:

    def __init__(self):
        self.Data = None

    def store(self, bulk_data):
        self.Data = bulk_data

    def matches(self, day_of_week, time):
        matching_restaurant_names = []

        for establishment in self.Data.Keys():
            if day_of_week in self.Data[establishment].Keys():
                start_time = self.Data[establishment][day_of_week].start
                end_time = self.Data[establishment][day_of_week].end
                if start_time <= time < end_time:
                    matching_restaurant_names.append(establishment)

        return None
