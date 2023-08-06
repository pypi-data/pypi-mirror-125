# bfd
from math import degrees, atan
from .config import BEARING


def get_bearing_from_deltas(deltas):
    # unpack the deltas
    delta_e = deltas[0]
    delta_n = deltas[1]
    # delta_el = deltas[2]

    # Check for E W, N S movement.
    if delta_n == 0:
        bearing = 90.0
        if delta_e < 0:
            bearing = 270.0

    elif delta_e == 0:
        bearing = 0.0
        if delta_n < 0:
            bearing = 180.0

    # Determine ordinary bearing.
    else:
        tan_results = delta_n / delta_e
        tan_results = atan(tan_results)
        tan_results = degrees(tan_results)

        if delta_e > 0 and delta_n > 0:
            bearing = 90 - abs(tan_results)
        # TODO refactor, chain.
        elif delta_e > 0 and delta_n < 0:
            bearing = 90 + abs(tan_results)
        elif delta_e < 0 and delta_n < 0:
            bearing = 270 - abs(tan_results)
        else:
            bearing = 270 + abs(tan_results)

        # TODO return as dictionary.
    return {BEARING: bearing}
