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
        return await this.apiClient.get('/menus');
    }

    async getMenuItemById(id) {
        if (!authService.isAuthenticated()) {
            throw new Error('Unauthorized');
        }
        const response = await  this.apiClient.get(`/menus/${id}`);
        if(response.status === 200) {
            return response.data;
        } else {
            return null;
        }
    }

    async createMenuItem(menuItemData, image) {
        if (!await authService.isAuthenticated() || await authService.getRole() !== 'admin') {
            console.log('Unauthorized', authService.getRole(), authService.isAuthenticated());
            throw new Error('Unauthorized');
        }

        // Debemos subir la imagen al servidor y obtener la URL de la imagen
        if (image instanceof File) {
            console.log("1", image.type);
            if (image.type.startsWith('image/')) {
                console.log("2", image.type);
                // Usamos la API en el endpoint /images    
                try {
                    const response = await this.apiClient.uploadFile('/images', image);
                    menuItemData.image = response.data.file_path;
                    console.log('Image uploaded:', response.data);
                } catch (error) {
                    console.error('Error uploading image:', error);
                    menuItemData.image = "";
                }
            } else {
                menuItemData.image = "";
            }
        }
        
        //debemos agregarle el .00 si no lo tiene
        if(!menuItemData.price.toString().includes('.')) {
            menuItemData.price = menuItemData.price + '.00';
        }



        //creamos un createMenuRequestDto
        const createMenuRequestDto = new CreateMenuRequestDto(menuItemData.name, menuItemData.description,menuItemData.price , menuItemData.category_id, menuItemData.image);
        

        const response = await this.apiClient.post('/menus', createMenuRequestDto);

        if(response.status === 201 || response.status === 200) {
            return true;
        } else {
            return false;
        }

    }

    async updateMenuItem(id, menuItemData, image, lastImage = "") {
        if (!await authService.isAuthenticated() || await authService.getRole() !== 'admin') {
            console.log('Unauthorized', await authService.getRole(), await authService.isAuthenticated());
            throw new Error('Unauthorized');
        }
        console.log('Updating menu item:', menuItemData);
    
        // Check if the image needs to be updated
        if (image && image instanceof File) {
            console.log("1", image.type);
            if (image.type.startsWith('image/')) {
                console.log("2", image.type);
                // Usamos la API en el endpoint /images    
                try {
                    const response = await this.apiClient.uploadFile('/images', image);
                    menuItemData.image = response.data.file_path;
                    console.log('Image uploaded:', response.data);
                } catch (error) {
                    console.error('Error uploading image:', error);
                    menuItemData.image = "";
                }
            } else {
                menuItemData.image = "";
            }
        } else {
            // Retain the existing image if no new image is provided
            menuItemData.image = lastImage.split("/").pop();
        }
    
        // Add .00 to the price if it doesn't have it
        if (!menuItemData.price.toString().includes('.')) {
            menuItemData.price = menuItemData.price + '.00';
        }
    
        // Create a createMenuRequestDto
        const createMenuRequestDto = new CreateMenuRequestDto(
            menuItemData.name,
            menuItemData.description,
            menuItemData.price,
            menuItemData.category_id,
            menuItemData.image
        );
    
        const response = await this.apiClient.put(`/menus/${id}`, createMenuRequestDto);
    
        if (response.status === 200) {
            return true;
        } else {
            return false;
        }
    }

    async getImagefromServer(filename){
        //retornamos la url de la imagen
        return `${config.apiBaseUrl}/images/${filename}`;
    }

    async deleteMenuItem(id) {
        if (!await authService.isAuthenticated() || await authService.getRole() !== 'admin') {
            console.log('Unauthorized', authService.getRole(), authService.isAuthenticated());
            throw new Error('Unauthorized');
        }
        return await  this.apiClient.delete(`/menus/${id}`);
    }

    async getCategories() {
        return await this.apiClient.get('/categories');
    }

    async getCategoryById(id) {
        return await this.apiClient.get(`/categories/${id}`);
    }

    async createCategory(categoryData) {
        if (!authService.isAuthenticated() || authService.getUserRole() !== 'admin') {
            throw new Error('Unauthorized');
        }
        return await this.apiClient.post('/categories', categoryData);
    }
}

const menuService = new MenuService();
export default menuService;