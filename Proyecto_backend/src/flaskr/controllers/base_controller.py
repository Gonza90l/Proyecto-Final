# app/controllers/base_controller.py
from flask import request
from flaskr.responses.api_response import ApiResponse
from injector import inject

class BaseController:
    
    def get_json_data(self):
        return request.json

    def get_query_params(self):
        return request.args

    def get_form_data(self):
        return request.form

    def get_headers(self):
        return request.headers

    def get_cookies(self):
        return request.cookies

    def respond_success(self, data=None, message="Success", status_code=200, metadata=None):
        return ApiResponse.success(data=data, message=message, status_code=status_code, metadata=metadata)

    def respond_error(self, message="An error occurred", status_code=400, errors=None):
        return ApiResponse.error(message=message, status_code=status_code, errors=errors)

