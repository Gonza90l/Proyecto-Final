# app/middlewares.py
from flask import request

def log_request():
    print(f"Request: {request.method} {request.path}")

def log_response(response):
    print(f"Response: {response.status}")
    return response