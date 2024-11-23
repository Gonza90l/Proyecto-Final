// Descripción: Servicio que se encarga de realizar las peticiones al backend relacionadas con las notificaciones
import ApiClient from './apiClient.js';
import authService from './authService.js';
import config from './config.js';

class NotificationsService {
    constructor() {}

    init() {}

    _getApiClient() {
        const token = authService.getToken();
        const apiClient = new ApiClient(config.apiBaseUrl);
        apiClient.token = token;
        return apiClient;
    }

    async getAllNotifications() {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        return await apiClient.get('/notifications');
    }

    async getNotificationById(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        return await apiClient.get(`/notifications/${id}`);
    }

    async createNotification(notificationData) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        return await apiClient.post('/notifications', notificationData);
    }

    async updateNotification(id, notificationData) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        return await apiClient.put(`/notifications/${id}`, notificationData);
    }

    async deleteNotification(id) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        return await apiClient.delete(`/notifications/${id}`);
    }

    async markNotificationAsRead(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        return await apiClient.put(`/notifications/${id}/read`);
    }
}

const notificationsService = new NotificationsService();
export default notificationsService;