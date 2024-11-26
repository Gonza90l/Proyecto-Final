// Tipo de instancia: Singleton
import ApiClient from './apiClient.js';
import authService from './authService.js';
import config from './config.js';

class StatisticsService {
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
    

    async getStatistics() {
        const apiClient = this._getApiClient();
        const response = await apiClient.get('/statistics');
        return response;
    }


}


const statisticsService = new StatisticsService();
export default statisticsService;
