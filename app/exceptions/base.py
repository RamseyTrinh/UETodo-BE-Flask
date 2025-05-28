from flask import jsonify
from werkzeug.exceptions import HTTPException


def base_exception(e):
    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = jsonify({"error": str(e)}).data
        response.content_type = "application/json"
        return response

    return jsonify({"error": "Internal server error.", "message": str(e)}), 500
