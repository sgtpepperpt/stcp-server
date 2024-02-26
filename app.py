import os

from flask import Flask, request
from flask_cors import CORS, cross_origin

from stcp.api import get_lines, get_line_directions, get_line_stops, get_stop_real_times
from src.stops import write_stops_file, read_stops_file, get_static_stop_data


app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/line')
@cross_origin(supports_credentials=True)
def all_lines():
    return get_lines()


@app.route('/line/<line_code>')
@cross_origin(supports_credentials=True)
def get_line(line_code: str):
    line = []
    directions = get_line_directions(line_code)
    for direction in directions:
        direction['stops'] = get_line_stops(line_code, direction['direction_code'])

        # append detailed stop data
        for i, stop in enumerate(direction['stops']):
            stop_code = stop['stop_code']
            direction['stops'][i] = get_static_stop_data(stop_code)

        line.append(direction)

    return line


@app.route('/stop')
@cross_origin(supports_credentials=True)
def all_stops():
    if not os.path.isfile('stops_data.json'):
        print('Writing stops file for the first time...')
        write_stops_file()
        print('Done')

    return read_stops_file()


@app.route('/stop/<stop_code>')
@cross_origin(supports_credentials=True)
def get_stop(stop_code: str):
    static_only = request.args.get('static_only', False)

    stop_data = get_static_stop_data(stop_code)

    if not static_only:
        timetable = get_stop_real_times(stop_code, use_hash_cache=False)

        # append next buses to each line of the stop
        # create a map of all the lines and their departures
        line_departures = {}
        for bus in timetable:
            line_code = bus['line_code']
            if line_code not in line_departures:
                line_departures[line_code] = []

            line_departures[line_code].append(bus['time'])

        # append the departures to their respective line
        for line in stop_data['lines']:
            line_code = line['line_code']
            line['next'] = line_departures[line_code] if line_code in line_departures else []

    return stop_data


@app.route('/time/<stop_code>')
@cross_origin(supports_credentials=True)
def get_timetable(stop_code: str):
    return get_stop_real_times(stop_code, use_hash_cache=False)


if __name__ == '__main__':
    app.run()
