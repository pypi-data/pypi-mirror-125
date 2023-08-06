# dec


def to_decimal_degrees(dms):
    # Converts degrees minutes and seconds to decimal degrees.

    # Isolate the degrees component.
    d_deg = int(dms)

    # Isolate the minutes component and convert.
    d_min = (int((dms - d_deg) * 100)) / 60

    # Isolate the seconds component and convert
    d_sec = ((dms * 100 - int(dms * 100)) * 100) / 3600

    return d_deg + d_min + d_sec
