// Tipo de instancia: Singleton

import ApiClient from './apiClient.js';
import authService from './authService.js';
import CreateMenuRequestDto  from './dtos/CreateMenuRquestDto.js';
import config from './config.js'; // Importa la configuración


class MenuService {
    constructor() {
        this.apiClient = new ApiClient(config.apiBaseUrl);
        this.token = null;
    }

     init() {
        this.token = localStorage.getItem('authToken');
        this.tokenExpiry = localStorage.getItem('tokenExpiry');
        if (this.token && this.tokenExpiry) {
            console.log('Token found:', this.token);
            this.apiClient.token = this.token; // Actualiza el token en ApiClient
        } else {
            console.log('No token found, user is not authenticated.');
        }
    }
    
    async getAllMenuItems() {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await apiClient.get('/menus');
    }

    async getMenuItemById(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        return await  this.apiClient.get(`/menus/${id}`);
    }

    async createMenuItem(menuItemData) {
        if (!await authService.isAuthenticated() || await authService.getRole() !== 'admin') {
            console.log('Unauthorized', authService.getRole(), authService.isAuthenticated());
            throw new Error('Unauthorized');
        }

        //debemos subir la imagen al servidor y obtener la URL de la imagen
        if(menuItemData.image instanceof File) {
            if(!menuItemData.image.type.startsWith('image/')) {
                const formData = new FormData();
                formData.append('image', menuItemData.image);
                const response = await fetch(config.apiBaseUrl + '/images', {
                    method: 'POST',
                    headers: {
                        Authorization: `Bearer ${authService.getAuthToken()}`
                    },
                    body: formData
                });

                const responseData = await response.json();
                menuItemData.image = responseData.imageUrl;
            }
        }
        
        //debemos agregarle el .00 si no lo tiene
        if(!menuItemData.price.toString().includes('.')) {
            menuItemData.price = menuItemData.price + '.00';
        }



        //creamos un createMenuRequestDto
        const createMenuRequestDto = new CreateMenuRequestDto(menuItemData.name, menuItemData.description,menuItemData.price , menuItemData.category_id, "");
        
        console.log('createMenuRequestDto', createMenuRequestDto);

        return await this.apiClient.post('/menus', createMenuRequestDto);
    }

    async updateMenuItem(id, menuItemData) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await  this.apiClient.put(`/menu/${id}`, menuItemData);
    }

    async deleteMenuItem(id) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await  this.apiClient.delete(`/menu/${id}`);
    }
}

const menuService = new MenuService();
export default menuService;