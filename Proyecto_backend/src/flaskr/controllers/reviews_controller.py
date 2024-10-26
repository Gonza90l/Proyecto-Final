from app.controllers.base_controller import BaseController
from app.services.reviews_service import ReviewsService
from app.auth import token_required
from injector import inject

class ReviewsController(BaseController):
    @inject
    def __init__(self, reviews_service: ReviewsService):
        self.reviews_service = reviews_service

    @token_required
    def get_reviews(self):
        reviews = self.reviews_service.get_reviews()
        return self.respond_success(data=reviews)

    @token_required
    def get_review(self, review_id):
        review = self.reviews_service.get_review(review_id)
        return self.respond_success(data=review)

    @token_required
    def get_reviews_by_user(self, user_id):
        reviews = self.reviews_service.get_reviews_by_user(user_id)
        return self.respond_success(data=reviews)

    @token_required
    def create_review(self):
        data = self.get_json_data()
        review = self.reviews_service.create_review(data)
        return self.respond_success(data=review)

    @token_required
    def delete_review(self, review_id):
        review = self.reviews_service.delete_review(review_id)
        return self.respond_success(data=review)