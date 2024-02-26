import json
import os

from stcp.api import get_stop_data
from stcp.util import get_all_stops


def write_stops_file(filename='stops_data.json'):
    from stcp.api import get_stop_data

    with open(filename, 'w') as file:
        stop_data = [get_stop_data(stop_code) for stop_code in get_all_stops()]
        json.dump(stop_data, file)


def read_stops_file(filename='stops_data.json'):
    with open(filename, 'r') as file:
        return json.loads(file.read())


def get_static_stop_data(stop_code):
    if os.path.isfile('stops_data.json'):
        all_stops = read_stops_file()
        for stop in all_stops:
            if stop_code == stop['stop_code']:
                return stop

    return get_stop_data(stop_code)
