def is_datetime(word):
    if word.lower().find("date") >= 0:
        return True
    if word.lower().find("datetime") >= 0:
        return True
    else:
        return False

def transform_range(value, range):
    NewRange = range[1] - range[0]
    return ((value * NewRange) / 100) + range[0]

def reverse_transform_range(value, range):
        OldRange = range[1] - range[0]
        return (((value - range[0]) * 100) / OldRange)