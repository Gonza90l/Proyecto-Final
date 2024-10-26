// Tipo de instancia: Singleton

class ReviewsService {
    constructor() {
        
    }

    init() {

    }
    
    async getAllReviews() {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.get('/reviews');
    }

    async getReviewById(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.get(`/reviews/${id}`);
    }

    async createReview(reviewData) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.post('/reviews', reviewData);
    }

    async updateReview(id, reviewData) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.put(`/reviews/${id}`, reviewData);
    }

    async deleteReview(id) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.delete(`/reviews/${id}`);
    }
}

const reviewsService = new ReviewsService();
export default reviewsService;