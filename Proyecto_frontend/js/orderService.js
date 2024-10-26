// Tipo de instancia: Singleton

class OrdersService {

    constructor() {
        
    }

    init() {

    }

    async getAllOrders() {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.get('/orders');
    }

    async getOrderById(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.get(`/orders/${id}`);
    }

    async createOrder(orderData) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.post('/orders', orderData);
    }

    async updateOrder(id, orderData) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.put(`/orders/${id}`, orderData);
    }

    async deleteOrder(id) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.delete(`/orders/${id}`);
    }
}

const ordersService = new OrdersService();
export default ordersService;