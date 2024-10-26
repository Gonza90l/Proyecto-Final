// Tipo de instancia: Singleton

class NotificationsService {
    constructor() {
        
    }

    init() {

    }

    async getAllNotifications() {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.get('/notifications');
    }

    async getNotificationById(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.get(`/notifications/${id}`);
    }

    async createNotification(notificationData) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.post('/notifications', notificationData);
    }

    async updateNotification(id, notificationData) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.put(`/notifications/${id}`, notificationData);
    }

    async deleteNotification(id) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.delete(`/notifications/${id}`);
    }
}

const notificationsService = new NotificationsService();
export default notificationsService;