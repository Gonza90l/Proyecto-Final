from flaskr.services.review_service import ReviewService
from flaskr.controllers.base_controller import BaseController
from flask_injector import inject
from flaskr.auth import token_required, role_required
from flaskr.dtos.create_review_request_dto import CreateReviewRequestDTO

class ReviewController(BaseController):
    @inject
    def __init__(self, review_service: ReviewService):
        """
        Constructor de la clase ReviewController.
        
        :param review_service: Servicio de reseñas inyectado.
        """
        self.review_service = review_service

    @token_required
    def get_review_by_id(self, review_id):
        """
        Obtiene una reseña específica por su ID.

        :param review_id: ID de la reseña.
        :return: Respuesta JSON con los datos de la reseña.
        """
        try:
            review = self.review_service.get_review_by_id(review_id)
            if not review:
                return self.respond_error(message="Review not found", status_code=404)
            return self.respond_success(data=review)
        except Exception as e:
            return self.respond_error(message=str(e))

    @role_required('USER')
    def create_review(self):
        """
        Crea una nueva reseña.

        :return: Respuesta JSON con los datos de la reseña creada.
        """
        try:
            # Obtenemos la data del body
            data = self.get_json_data()
            print(data)
            # Convertimos la data a CreateReviewRequestDTO
            create_review_request_dto, errors = CreateReviewRequestDTO.from_json(data)
            if errors:
                return self.respond_error(message="Validation errors", errors=errors, status_code=422)

            review = self.review_service.create_review(
                create_review_request_dto.id,
                create_review_request_dto.order_id,
                create_review_request_dto.rating,
                create_review_request_dto.review
            )
            return self.respond_success(data=review)
        except Exception as e:
            return self.respond_error(message=str(e))

    def update_review(self, review_id):
        """
        Método no permitido para actualizar una reseña.

        :param review_id: ID de la reseña.
        :return: Respuesta JSON con el mensaje de error.
        """
        return self.respond_error(message="Method not allowed", status_code=405)

    def delete_review(self, review_id):
        """
        Método no permitido para eliminar una reseña.

        :param review_id: ID de la reseña.
        :return: Respuesta JSON con el mensaje de error.
        """
        return self.respond_error(message="Method not allowed", status_code=405)

    @token_required
    def get_review_by_order_id(self, order_id):
        """
        Obtiene una reseña específica por el ID de la orden.

        :param order_id: ID de la orden.
        :return: Respuesta JSON con los datos de la reseña.
        """
        try:
            review = self.review_service.order_has_review(order_id)
            return self.respond_success(data=review)
        except Exception as e:
            return self.respond_error(message=str(e))