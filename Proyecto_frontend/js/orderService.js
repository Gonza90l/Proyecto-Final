
import authService from './authService.js';
import ApiClient from './apiClient.js';
import config from './config.js';
import { routerInstance } from './router.js';


class OrdersService {

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

    async getAllOrders() {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        const response = await apiClient.get('/orders');
        if (response.status === 200) {
            return response.data;
        } else {
            return null;
        }
    }

    async getOrderById(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        const response = await apiClient.get(`/orders/${id}`);
        if (response.status === 200) {
            return response.data;
        } else {
            return null;
        }
    }

    async createOrder(orderData) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        //si es exitoso devioolvemos el id del pedido
        const response = await apiClient.post('/orders', orderData);
        if (response.status === 201 || response.status === 200) {
            return response.data;
        } else {
            return null;
        }
        
    }

    async updateOrder(id, orderData) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
    
        // Quitamos los campos que no son permitidos
        if (orderData.created_at) {
            delete orderData.created_at;
        }
        if (orderData.id) {
            delete orderData.id;
        }
    
        // Transformamos los datos para que coincidan con los DTOs esperados
        const transformedOrderData = {
            user_id: orderData.user_id,
            total: parseFloat(orderData.total),
            status: orderData.status,
            order_items: orderData.order_items.map(item => ({
                menu_id: item.item.id,
                quantity: item.quantity
            }))
        };
    
        console.log(transformedOrderData);
    
        const apiClient = this._getApiClient();
        return await apiClient.put(`/orders/${id}`, transformedOrderData);
    }

    async deleteOrder(id) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        const apiClient = this._getApiClient();
        return await apiClient.delete(`/orders/${id}`);
    }

    //simulamos un push de la pasarela de pago
    async sendIPNToServer(ipnData) {
        try{
            const apiClient = this._getApiClient();
            const response = await apiClient.post(`/ipn`, ipnData);
            if (response.status === 201 || response.status === 200) {
                return true;
            } else {
                return false;
            }
        }catch(e){
            console.error(e);
            return false;
        }
    }
}

const ordersService = new OrdersService();
export default ordersService;