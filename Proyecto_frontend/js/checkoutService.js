// Tipo de instancia: Singleton

class CheckoutService {
    constructor() {
        
    }

    init() {

    }
    
    async initiateCheckout(checkoutData) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.post('/checkout', checkoutData);
    }

    async getCheckoutStatus(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.get(`/checkout/${id}`);
    }

    async completeCheckout(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.put(`/checkout/${id}/complete`);
    }
}

const checkoutService = new CheckoutService();
export default checkoutService; 