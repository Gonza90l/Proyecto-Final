from flaskr.controllers.base_controller import BaseController
from flaskr.services.image_service import ImageService
from flask_injector import inject
from flask import request, jsonify

class ImageController(BaseController):
    @inject
    def __init__(self, image_service: ImageService):
        """
        Constructor de la clase ImageController.
        
        :param image_service: Servicio de imágenes inyectado.
        """
        self._image_service = image_service

    def upload_image(self):
        """
        Maneja la subida de una imagen.

        :return: Respuesta JSON con el resultado de la operación.
        """
        if 'file' not in request.files:
            return jsonify({'error': 'No se encontró la parte del archivo'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No se seleccionó ningún archivo'}), 400
        try:
            file_path = self._image_service.upload_image(file)
            return self.respond_success(data={'file_path': file_path})
        except ValueError as e:
            return self.respond_error(message=str(e), status_code=400)
        except Exception as e:
            return self.respond_error(message='Error interno del servidor', status_code=500)

    def get_image(self, filename):
        """
        Obtiene una imagen por su nombre de archivo.

        :param filename: Nombre del archivo de la imagen.
        :return: Imagen solicitada.
        """
        try:
            return self._image_service.get_image(filename)
        except FileNotFoundError:
            return self.respond_error(message='Archivo no encontrado', status_code=404)
        except Exception as e:
            return self.respond_error(message='Error interno del servidor', status_code=500)

    def delete_image(self, filename):
        """
        Elimina una imagen por su nombre de archivo.

        :param filename: Nombre del archivo de la imagen a eliminar.
        :return: Respuesta JSON con el resultado de la operación.
        """
        try:
            return self._image_service.delete_image(filename)
        except FileNotFoundError:
            return self.respond_error(message='Archivo no encontrado', status_code=404)
        except Exception as e:
            return self.respond_error(message='Error interno del servidor', status_code=500)