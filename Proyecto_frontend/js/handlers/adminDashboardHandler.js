import statisticsService from '../statisticsService.js';
import { routerInstance } from '../router.js';
import authService from '../authService.js';

class AdminDashboardHandler {
    constructor() {
        this.statisticsService = statisticsService;
    }

    async init() {
        //si es aDMIN
        if (await authService.getRole() != 'admin') {
           return;
        }
        try {
            const response = await this.statisticsService.getStatistics();
            const statistics = response.data;
            this.renderStatistics(statistics);
        }catch (error) {
        }
    }

    renderStatistics(statistics) {
        const totalOrdersElement = document.getElementById('total-orders');
        const totalRevenueElement = document.getElementById('total-revenue');
        const pendingOrdersElement = document.getElementById('pending-orders');
    
        if (totalOrdersElement) {
            totalOrdersElement.textContent = statistics.total_orders;
        }
    
        if (totalRevenueElement) {
            totalRevenueElement.textContent = `$${parseFloat(statistics.total_amount).toFixed(2)}`;
        }
    
        if (pendingOrdersElement) {
            pendingOrdersElement.textContent = statistics.pending_orders;
        }
    }
}

export default AdminDashboardHandler;