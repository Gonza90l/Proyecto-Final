// Tipo de instancia: Singleton

class MenuService {
    constructor() {
        this.token = null;
    }

    init() {

    }
    
    async getAllMenuItems() {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.get('/menu');
    }

    async getMenuItemById(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.get(`/menu/${id}`);
    }

    async createMenuItem(menuItemData) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.post('/menu', menuItemData);
    }

    async updateMenuItem(id, menuItemData) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.put(`/menu/${id}`, menuItemData);
    }

    async deleteMenuItem(id) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await apiClient.delete(`/menu/${id}`);
    }
}

const menuService = new MenuService();
export default menuService;