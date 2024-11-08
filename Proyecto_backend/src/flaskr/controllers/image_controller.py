from flaskr.controllers.base_controller import BaseController
from flaskr.services.image_service import ImageService
from flask_injector import inject
from flask import request, jsonify

class ImageController(BaseController):
    @inject
    def __init__(self, image_service: ImageService):
        self._image_service = image_service

    def upload_image(self):
        if 'file' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        try:
            file_path = self._image_service.upload_image(file)
            return self.respond_success(data={'file_path': file_path})
        except ValueError as e:
            return  self.respond_error(message=str(e), status_code=400)

    def get_image(self, filename):
        return self._image_service.get_image(filename)

    def delete_image(self, filename):
        return self._image_service.delete_image(filename)