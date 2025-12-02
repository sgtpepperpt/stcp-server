import os

from flask import Flask, request
from flask_cors import CORS, cross_origin
from stcp.routes import get_routes, get_route_directions, get_route_stops
from stcp.stops import get_stop_real_time
from stcp.util import get_stop_route_departures

from src.stops import write_stops_file, read_stops_file, get_static_stop_data

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/route')
@cross_origin(supports_credentials=True)
def all_routes():
    return get_routes()


@app.route('/route/<route_slug>')
@cross_origin(supports_credentials=True)
def get_route(route_slug: str):
    route = []
    directions = get_route_directions(route_slug)
    for direction in directions:
        direction['stops'] = get_route_stops(route_slug, direction['direction_id'])

        # append detailed stop data
        for i, stop in enumerate(direction['stops']):
            stop_id = stop['stop_id']
            direction['stops'][i] = get_static_stop_data(stop_id)

        route.append(direction)

    return route


@app.route('/stop')
@cross_origin(supports_credentials=True)
def all_stops():
    if not os.path.isfile('stops_data.json'):
        print('Writing stops file for the first time...')
        write_stops_file()
        print('Done')

    return read_stops_file()


@app.route('/stop/<stop_id>')
@cross_origin(supports_credentials=True)
def get_stop(stop_id: str):
    stop_id = stop_id.upper()

    static_only = request.args.get('static_only', False)

    stop_data = get_static_stop_data(stop_id)

    if not static_only:
        # append the departures to their respective line
        line_departures = get_stop_route_departures(stop_id)

        for route in stop_data['routes']:
            route_id = route['route_id']
            route['next'] = line_departures[route_id] if route_id in line_departures else []

    return stop_data


@app.route('/time/<stop_id>')
@cross_origin(supports_credentials=True)
def get_timetable(stop_id: str):
    stop_id = stop_id.upper()
    return get_stop_real_time(stop_id)


if __name__ == '__main__':
    app.run()
