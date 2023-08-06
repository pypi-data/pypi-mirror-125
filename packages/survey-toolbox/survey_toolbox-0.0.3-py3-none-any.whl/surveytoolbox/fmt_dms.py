# fmt_dms


def format_as_dms(dms):
    # Formats degrees minutes seconds for readability and returns.
    # Isolate degrees.
    d_deg = int(dms)

    # Isolate minutes.
    d_min = (int((dms - d_deg) * 100))

    # Isolate seconds.
    d_sec = ((dms * 100 - int(dms * 100)) * 100)

    # Format and return.
    return f"{d_deg}° {d_min}' {d_sec}\""
