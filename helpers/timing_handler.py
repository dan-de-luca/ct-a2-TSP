import time

def duration_hms(start_time, end_time) -> str:
    duration = end_time - start_time
    
    # Extract milliseconds
    milliseconds = int((duration - int(duration)) * 1000)
    
    # Convert total seconds to hours, minutes, and seconds
    hours, remainder = divmod(duration, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # Format the time string as HH:MM:SS.mmm
    return time.strftime("%H:%M:%S", time.gmtime(duration)) + "." + str(milliseconds)
    
    # return time.strftime("%H:%M:%S", time.gmtime(duration))


def duration_s(start_time, end_time) -> float:
    duration = end_time - start_time
    return duration
