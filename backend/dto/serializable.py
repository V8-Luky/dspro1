from flask import jsonify


class Serializable:
    def to_json(self):
        return jsonify(vars(self))
