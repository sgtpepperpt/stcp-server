from flask import Flask
from stcp.api import get_lines, get_line_directions, get_line_stops, get_stop_data, get_stop_real_times

app = Flask(__name__)


@app.route('/line')
def all_lines():
    return get_lines()


@app.route('/line/<line_code>')
def line_directions(line_code: str):
    return get_line_directions(line_code)


@app.route('/line/<line_code>/<direction_code>')
def line(line_code: str, direction_code: str):
    return get_line_stops(line_code, direction_code)


@app.route('/stop/<stop_code>')
def stop(stop_code: str):
    return get_stop_data(stop_code)


@app.route('/stop/<stop_code>/times')
def times(stop_code: str):
    return get_stop_real_times(stop_code, use_hash_cache=False)


if __name__ == '__main__':
    app.run()
