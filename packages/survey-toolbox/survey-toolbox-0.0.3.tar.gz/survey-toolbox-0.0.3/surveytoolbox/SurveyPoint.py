from datetime import datetime
from .commonCalculations import EASTING as EASTING
from .commonCalculations import NORTHING as NORTHING
from .commonCalculations import ELEVATION as ELEVATION

STATUS_ACTIVE = True
STATUS_INACTIVE = False


class NewSurveyPoint:
    """A Point object class"""
    def __init__(self, point_name):
        self.oid = "uid4"
        self.pointName = point_name
        self.featureCode = ""
        self.vertex = {EASTING: 0.000, NORTHING: 0.000, ELEVATION: 0.000}
        self.createdDTG = datetime.now()
        self.status = STATUS_ACTIVE
        self.clonedFrom = False

    def set_point_name(self, point_name):
        # TODO test for invalid characters (ie spaces)
        self.pointName = point_name
        return True

    def get_point_name(self):
        return self.pointName

    def set_feature_code(self, feature_code):
        self.featureCode = feature_code
        return True

    def get_feature_code(self):
        return self.featureCode

    def set_vertex(self, vertex):
        # TODO Test validity.
        for key, value in vertex.items():
            self.vertex[key] = value
        return True

    def get_vertex(self):
        return self.vertex

    def set_created_dtg(self, created_dtg):
        # TODO Test validity.
        self.createdDTG = created_dtg
        return True

    def get_created_dtg(self):
        return self.createdDTG

    def set_status(self, status):
        # TODO test validity. Limit options.
        self.status = status
        return True

    def get_status(self):
        return self.status

    def set_cloned_from(self, cloned_from):
        # TODO Test validity.
        self.clonedFrom = cloned_from
        return True

    def get_cloned_from(self):
        return self.clonedFrom
