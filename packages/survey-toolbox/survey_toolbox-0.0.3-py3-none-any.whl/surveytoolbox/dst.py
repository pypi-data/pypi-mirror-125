# dst

def distance_from_speed_and_time(movement_speed, movement_time):
    """Returns distance from speed and time"""
    return movement_time * movement_speed * 1000 / 3600


def time_to_target(movement_speed, movement_distance):
    """Returns time to target based on distance and speed"""
    return movement_distance / 1000 / movement_speed


def format_time_to_target(time_to_target_in):
    """Returns dhours, minutes, seconds"""
    time_to_target_h = int(time_to_target_in)
    time_to_target_m = (time_to_target_in * 60) % 60
    time_to_target_s = (time_to_target_in * 3600) % 60
    return [time_to_target_h, time_to_target_m, time_to_target_s]
