class NewPointStore:
    # TODO implement local database storage options.
    def __init__(self):
        self.point_store = {}
        self.number_points = 0

    def set_new_point(self, point):
        point_name = point.get_point_name()
        self.point_store[point_name] = point
        return True

    def get_point_store(self):
        return self.point_store
