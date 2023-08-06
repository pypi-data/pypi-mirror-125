# bdc
from .commonCalculations import get_deltas_from_coordinates
from .commonCalculations import get_distance_2d_from_deltas
from .commonCalculations import get_distance_3d_from_deltas
from .bfd import get_bearing_from_deltas


def bearing_distance_from_coordinates(from_coordinates, to_coordinates):
    # Return bearing and distance(s) from two sets of coordinates.
    # Determine deltas
    deltas = get_deltas_from_coordinates(from_coordinates, to_coordinates)
    # Determine bearing
    bearing = get_bearing_from_deltas(deltas)
    # Determine distances.
    dist_2d = get_distance_2d_from_deltas(deltas)
    dist_3d = get_distance_3d_from_deltas(deltas)

    # Merge the dictionaries and return.
    return {**bearing, **dist_2d, **dist_3d}
