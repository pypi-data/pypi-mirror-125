# dms


def to_deg_min_sec(dec):
    # Converts decimal degrees to degrees minutes seconds
    # Isolate the degrees.
    d_deg = int(dec)

    # Isolate and convert the minutes.
    d_min = int((dec - d_deg) * 60)

    # Isolate and convert the seconds.
    d_sec = (dec - d_deg - d_min / 60) * 3600

    return d_deg + d_min / 100 + d_sec / 10000
