// Tipo de instancia: Singleton
import ApiClient from './apiClient.js';
import authService from './authService.js';
import config from './config.js';

class ReviewsService {
    constructor() {
        
    }

    init() {

    }

    _getApiClient() {
        const token = authService.getToken();
        const apiClient = new ApiClient(config.apiBaseUrl);
        apiClient.token = token;
        return apiClient;
    }
    
    async getReviewById(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        const response = await apiClient.get(`/reviews/${id}`);
        return response.data;
    }

    async createReview(reviewData) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        return await apiClient.post('/reviews', reviewData);
    }

    async updateReview(id, reviewData) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        return await apiClient.put(`/reviews/${id}`, reviewData);
    }

    async deleteReview(id) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        return await apiClient.delete(`/reviews/${id}`);
    }

    async getReviewsForMenu(menuId) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        const response = await apiClient.get(`/reviews/${menuId}`);
        if (response.status !== 'success') {
            throw new Error('Failed to fetch reviews');
        }
        return response.data;
    }
}

const reviewsService = new ReviewsService();
export default reviewsService;