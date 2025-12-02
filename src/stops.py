import json
import os

from stcp.stops import get_stop_data, get_stops


def write_stops_file(filename='stops_data.json'):
    with open(filename, 'w') as file:
        stop_data = [get_stop_data(stop['stop_id']) for stop in get_stops()]
        json.dump(stop_data, file)


def read_stops_file(filename='stops_data.json'):
    with open(filename, 'r') as file:
        return json.loads(file.read())


def get_static_stop_data(stop_id):
    if os.path.isfile('stops_data.json'):
        all_stops = read_stops_file()
        try:
            for stop in all_stops:
                if stop_id == stop['stop_id']:
                    return stop
        except KeyError:
            pass

    return get_stop_data(stop_id)
