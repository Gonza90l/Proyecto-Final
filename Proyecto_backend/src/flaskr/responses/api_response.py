# app/api_response.py
from flask import jsonify

class ApiResponse:
    @staticmethod
    def success(data=None, message="Success", status_code=200, metadata=None):
        response = {
            "status": "success",
            "message": message,
            "data": data,
            "metadata": metadata
        }
        return jsonify(response), status_code

    @staticmethod
    def error(message="An error occurred", status_code=400, errors=None):
        response = {
            "status": "error",
            "message": message,
            "errors": errors,
            "data": None
        }
        return jsonify(response), status_code