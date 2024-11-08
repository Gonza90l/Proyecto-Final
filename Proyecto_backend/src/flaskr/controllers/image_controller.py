
from flaskr.controllers.base_controller import BaseController
from flaskr.services.image_service import ImageService
from flask_injector import inject

class ImageController(BaseController):
    @inject
    def __init__(self, image_service: ImageService):
        self._menu_service = menu_service

    def upload_image(self):
        file = request.files['file']
        return self._image_service.upload_image(file)

    def get_image(self, filename):
        return self._image_service.get_image(filename)

    def delete_image(self, filename):
        return self._image_service.delete_image(filename)


