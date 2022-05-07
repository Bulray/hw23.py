import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


def build_query(it, cmd, value):
    res = map(lambda v: v.strip(), it)
    if cmd == "filter":
        res = filter(lambda v, txt=value: txt in v, res)
    if cmd == "map":
        arg = int(value)
        res = map(lambda v, idx=arg: v.split(" ")[idx], res)
    if cmd == "unique":
        res = set(res)
    if cmd == "sort":
        reverse = value == "desc"
        res = sorted(res, reverse=reverse)
    if cmd == "limit":
        arg = int(value)
        res = list(res)[:arg]
    return res


@app.route("/perform_query")
def perform_query():
    try:
        cmd1 = request.args["cmd1"]
        cmd2 = request.args["cmd2"]
        value1 = request.args["value1"]

        value2 =request.args["value2"]
        file_name = request.args["file_name"]
    except KeyError:
        raise BadRequest

    file_path = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(file_path):
        return BadRequest(description=f"{file_name} was not found")


    with open(file_path) as fd:
        res = build_query(fd, cmd1, value1)
        res = build_query(res, cmd2, value2)
        content = '\n'.join(res)
        print(content)
    return app.response_class(content, content_type="text/plain")

if __name__ == '__main__':
    app.run(debug=True)