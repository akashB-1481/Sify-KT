from flask import Flask, request
import json
import os

app = Flask(__name__)

FILE = "/data/items.json"


def read_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []


def write_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)


# Health Probe Endpoint
@app.route("/health", methods=["GET"])
def health():
    return {"status": "UP"}, 200


# GET
@app.route("/api", methods=["GET"])
def get_items():
    return {"data": read_data()}


# POST
@app.route("/api", methods=["POST"])
def add_item():
    items = read_data()

    item = request.json
    items.append(item)

    write_data(items)

    return {"message": "added"}


# PUT
@app.route("/api/<int:id>", methods=["PUT"])
def update_item(id):
    items = read_data()

    if id >= len(items):
        return {"error": "not found"}, 404

    items[id] = request.json
    write_data(items)

    return {"message": "updated"}


# DELETE
@app.route("/api/<int:id>", methods=["DELETE"])
def delete_item(id):
    items = read_data()

    if id >= len(items):
        return {"error": "not found"}, 404

    items.pop(id)
    write_data(items)

    return {"message": "deleted"}


app.run(host="0.0.0.0", port=5000)