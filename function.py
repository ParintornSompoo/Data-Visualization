import pandas as pd
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

def get_filter_data(data, dimension_filter, measurement_filter):
    query = '' 
    original_columns = data.columns
    data.columns = [column.replace(" ", "_") for column in data.columns]
    data.columns = [column.replace("-", "_") for column in data.columns]
    data.columns = [column.replace("(", "_") for column in data.columns]
    data.columns = [column.replace(")", "") for column in data.columns]
    data.columns = [column.replace(",", "") for column in data.columns]
    # dimensions filter
    for key in dimension_filter:
        original_key = key
        key = key.replace(" ","_")
        key = key.replace("-","_")
        key = key.replace("(","_")
        key = key.replace(")","")
        key = key.replace(",","")
        query += f"{key} == ["
        for selected in dimension_filter[original_key]:
            if is_datetime(original_key):
                query += f'{selected},'
            else:
                query += f'"{selected}",'
        query += "] and "
    # measurements filter
    for key in measurement_filter:
        original_key = key
        key = key.replace(" ","_")
        key = key.replace("-","_")
        min = measurement_filter[key]["min"]
        max = measurement_filter[key]["max"]
        query += f"{key} >= {min} and {key} <= {max} and "
    if len(query) != 0:
        filtered_data = data.query(query[:-5])
        filtered_data.columns = original_columns
    else:
        filtered_data = data
    data.columns = original_columns
    return filtered_data