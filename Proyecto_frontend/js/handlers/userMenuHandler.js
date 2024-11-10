import menuService from '../menuService.js';
import { routerInstance } from '../router.js';
import cart from '../cart.js';
import authService from '../authService.js';

class UserMenuHandler {

    async init() {
        this.loadMenus();
    }

    async loadMenus() {
        if(await authService.isAuthenticated()){
            try {
                const menuItems = await menuService.getAllMenuItems();
                this.renderMenu(menuItems.data);
            } catch (error) {
                console.error('Error fetching menu items:', error);
            }
        }
    }

    async renderMenu(menuItems) {
        this.menuSection = document.querySelector('.client-menu-section');
        if(this.menuSection) {
            const menuHtml = await Promise.all(menuItems.map(async item => `
                <article>
                    <head>
                        <h2>${item.name}</h2>
                        <p>Calificación <span class="rating">${item.rating}/5</span></p> 
                        <a href="#" onclick="alert('comentarios')" class="btn btn-primary">Ver comentarios</a>
                    </head>
                    <div>
                        <img src="${await menuService.getImagefromServer(item.photo)}" alt="Imagen de la comida">
                        <h3>Descripción</h3>
                        <p>${item.description}</p>
                    </div>
                    <footer>
                        <input type="number" min="1" max="99" value="1" class="quantity-input">
                        <button class="btn btn-primary" data-id="${item.id}">Añadir</button>
                    </footer>
                </article>
            `));
            this.menuSection.innerHTML = menuHtml.join('');
    
            //console log para ver menu items
            console.log(menuItems);
    
            // Add event listeners to "Añadir" buttons
            this.menuSection.querySelectorAll('.btn.btn-primary').forEach(button => {
                button.addEventListener('click', (event) => {
                    const itemId = event.target.getAttribute('data-id');
                    const item = menuItems.find(item => item.id == itemId);
                    if (!item) {
                        console.error(`Item with id ${itemId} not found`);
                        return;
                    }
                    const quantityInput = event.target.closest('article').querySelector('.quantity-input');
                    const quantity = parseInt(quantityInput.value, 10);
                    for (let i = 0; i < quantity; i++) {
                        console.log('Adding item to cart:', item);
                        cart.addItem(item);
                    }
                });
            });
        }
    }
}

export default UserMenuHandler;