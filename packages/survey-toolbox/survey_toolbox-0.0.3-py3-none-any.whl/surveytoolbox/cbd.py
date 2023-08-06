#  cbd
from .commonCalculations import get_deltas_from_bearing_distance
from .commonCalculations import get_coordinates_from_deltas


def coordinates_from_bearing_distance(from_coordinates, bearing, distance_2d):
    # Return coordinates from bearing and distance
    deltas = get_deltas_from_bearing_distance(bearing, distance_2d)
    new_coords = get_coordinates_from_deltas(from_coordinates, deltas)
    return new_coords
