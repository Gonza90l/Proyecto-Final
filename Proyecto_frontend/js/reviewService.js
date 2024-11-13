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

        //enviamos una a una las reviews
        for (let i = 0; i < reviewData.length; i++) {
            const apiClient = this._getApiClient();
            await apiClient.post('/reviews', reviewData[i]);
        }
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

    //averiguamos al endpoint get_review_by_order_id si poseemos una review para un pedido
    async getReviewByOrderId(orderId) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        const response = await apiClient.get(`/orders/${orderId}/review`);
        console.log(response);
        return response.data; // Devuelve solo el valor de data
    }
    
}

const reviewsService = new ReviewsService();
export default reviewsService;