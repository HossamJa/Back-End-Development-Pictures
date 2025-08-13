from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################

@app.route("/picture", methods=["GET"])
def get_pictures():
    """Return all the pictures"""
    return jsonify(data), 200

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    """Return a picture by ID"""
    for picture in data:
        if picture["id"] == id:
            return jsonify(picture), 200
    abort(404, f"Picture with ID {id} was not found!")


######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    """Create new picture"""
    picture_data = request.json
    for pic in data:
        if pic["id"] == picture_data["id"]:
            return {"Message": f"picture with id {picture_data['id']} already present"}, 302
    
    data.append(picture_data)
    return picture_data, 201

######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    """ Update an existing picture"""
    for index, pic in enumerate(data):
        if pic["id"] == id:
            data[index] = request.json
            return pic, 201

    abort(404, f"Picture with ID {id} was not found!")


######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    """ Delete an existing picture"""
    for index, pic in enumerate(data):
        if pic["id"] == id:
            del(data[index])
            return "", 204

    abort(404, f"Picture with ID {id} was not found!")
