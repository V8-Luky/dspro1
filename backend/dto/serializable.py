"""This module helps to bring objects into a format applicable for the web api."""

from flask import jsonify


class Serializable:
    """Represents an object that can be converted to JSON."""

    def to_json(self):
        """Converts the object to a flask compatible JSON object.
        By default, it returns all the attributes of the object.
        """
        return jsonify(vars(self))
