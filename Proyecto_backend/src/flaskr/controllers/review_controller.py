from flaskr.services.review_service import ReviewService
from flaskr.controllers.base_controller import BaseController
from flask_injector import inject

class ReviewController(BaseController):
    @inject
    def __init__(self, review_service: ReviewService):
        self.review_service = review_service

    def get_review_by_id(self, review_id):
        try:
            review = self.review_service.get_review_by_id(review_id)
            if not review:
                return self.respond_error(message="Review not found", status_code=404)
            return self.respond_success(data=review)
        except Exception as e:
            return self.respond_error(message=str(e))

    def create_review(self):
        try:
            review = self.review_service.create_review()
            return self.respond_success(data=review)
        except Exception as e:
            return self.respond_error(message=str(e))

    def update_review(self, review_id):
        try:
            review = self.review_service.update_review(review_id)
            return self.respond_success(data=review)
        except Exception as e:
            return self.respond_error(message=str(e))

    def delete_review(self, review_id):
        try:
            result = self.review_service.delete_review(review_id)
            return self.respond_success(data=result)
        except Exception as e:
            return self.respond_error(message=str(e))