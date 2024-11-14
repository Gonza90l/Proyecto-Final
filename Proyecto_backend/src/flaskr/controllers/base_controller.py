from flask import request
from flaskr.responses.api_response import ApiResponse

class BaseController:
    """
    Clase base para los controladores, proporciona métodos comunes para manejar solicitudes y respuestas.
    """
    
    def get_json_data(self):
        """
        Obtiene los datos JSON de la solicitud.

        :return: Datos JSON de la solicitud.
        """
        return request.json

    def get_query_params(self):
        """
        Obtiene los parámetros de consulta de la solicitud.

        :return: Parámetros de consulta de la solicitud.
        """
        return request.args

    def get_form_data(self):
        """
        Obtiene los datos del formulario de la solicitud.

        :return: Datos del formulario de la solicitud.
        """
        return request.form

    def get_headers(self):
        """
        Obtiene los encabezados de la solicitud.

        :return: Encabezados de la solicitud.
        """
        return request.headers

    def get_cookies(self):
        """
        Obtiene las cookies de la solicitud.

        :return: Cookies de la solicitud.
        """
        return request.cookies

    def get_files(self):
        """
        Obtiene los archivos de la solicitud.

        :return: Archivos de la solicitud.
        """
        return request.files

    def respond_success(self, data=None, message="Success", status_code=200, metadata=None):
        """
        Genera una respuesta exitosa.

        :param data: Datos a incluir en la respuesta.
        :param message: Mensaje de éxito.
        :param status_code: Código de estado HTTP.
        :param metadata: Metadatos adicionales.
        :return: Respuesta JSON de éxito.
        """
        return ApiResponse.success(data=data, message=message, status_code=status_code, metadata=metadata)

    def respond_error(self, message="An error occurred", status_code=400, errors=None):
        """
        Genera una respuesta de error.

        :param message: Mensaje de error.
        :param status_code: Código de estado HTTP.
        :param errors: Errores adicionales.
        :return: Respuesta JSON de error.
        """
        return ApiResponse.error(message=message, status_code=status_code, errors=errors)