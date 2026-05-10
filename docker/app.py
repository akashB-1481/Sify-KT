from flask import Flask, request
import json
import os

app = Flask(__name__)

FILE = "/data/items.json"

# To check for the file readiness

def read_data():
    if os.path.exists(FILE):
        with open(FILE, "r") as f:
            return json.load(f)
    return []

def write_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f)

# Adding Method for GET 

@app.route("/api", methods=["GET"])
def get_items():
    return {"data": read_data()}

#Adding Method for POST 

@app.route("/api", methods=["POST"])
def add_item():
    items = read_data()

    item = request.json
    items.append(item)

    write_data(items)

    return {"message": "added"}

@app.route("/api/<int:id>", methods=["PUT"])
def update_item(id):
    items = read_data()

    if id >= len(items):
        return {"error": "not found"}, 404

    items[id] = request.json
    write_data(items)

    return {"message": "updated"}

# Adding Method for Deletion

@app.route("/api/<int:id>", methods=["DELETE"])
def delete_item(id):
    items = read_data()

    if id >= len(items):
        return {"error": "not found"}, 404

    items.pop(id)
    write_data(items)

    return {"message": "deleted"}

app.run(host="0.0.0.0", port=5000)
