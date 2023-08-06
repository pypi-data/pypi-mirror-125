import math

from .config import EASTING, NORTHING, ELEVATION, DIST_2D, DIST_3D

# TODO separate these so each method can be tweaked without tweaking the whole.
# Do the math


def get_deltas_from_coordinates(from_coordinates, to_coordinates):
    # difference between both sets of coordinates.
    delta_e = to_coordinates[EASTING] - from_coordinates[EASTING]
    delta_n = to_coordinates[NORTHING] - from_coordinates[NORTHING]
    delta_el = to_coordinates[ELEVATION] - from_coordinates[ELEVATION]
    print (delta_e, delta_n, delta_el)
    return delta_e, delta_n, delta_el


def get_deltas_from_bearing_distance(bearing, distance_2d):
    # Creates deltas from bearing and distance
    delta_e = distance_2d * (math.sin(math.radians(bearing)))
    delta_n = distance_2d * (math.cos(math.radians(bearing)))
    delta_el = 0.0
    # TODO requires vertical bearing and distance for delta_el.
    # TODO refactor o return values in dictionary.
    return delta_e, delta_n, delta_el


def get_coordinates_from_deltas(from_coordinates, deltas):
    # Return new coords from deltas.
    return {
        EASTING: from_coordinates[EASTING] + deltas[0],
        NORTHING: from_coordinates[NORTHING] + deltas[1],
        ELEVATION: from_coordinates[ELEVATION] + deltas[2]
    }


def get_distance_2d_from_deltas(deltas):
    # Determine the distance. (2D)
    delta_e = deltas[0]
    delta_n = deltas[1]
    distance_2d = math.sqrt((delta_e ** 2 + delta_n ** 2))
    return {DIST_2D: distance_2d}


def get_distance_3d_from_deltas(deltas):
    # Determine the distance. (3D)
    delta_e = deltas[0]
    delta_n = deltas[1]
    delta_el = deltas[2]
    distance_3d = math.sqrt(delta_e ** 2 + delta_n ** 2 + delta_el ** 2)
    return {DIST_3D: distance_3d}
