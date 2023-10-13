import time

def duration_hms(start_time, end_time) -> str:
    duration = end_time - start_time
    return time.strftime("%H:%M:%S", time.gmtime(duration))
