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

            const categoriesResponse = await menuService.getCategories();
            const categories = categoriesResponse.data;

            // Crear un mapa de categorías para un acceso rápido
            const categoryMap = {};
            if (Array.isArray(categories)) {
                categories.forEach((category) => {
                    categoryMap[category.id] = category.name;
                });
            }

            // Agrupar los elementos del menú por categoría
            const groupedItems = menuItems.reduce((groups, item, index) => {
                const category = categoryMap[item.category_id] || 'Sin categoría';
                if (!groups[category]) {
                    groups[category] = [];
                }
                groups[category].push(item);
                return groups;
            }, {});
            // Obtener las URLs de las imágenes
            const imageUrls = await Promise.all(menuItems.map(item => menuService.getImagefromServer(item.photo)));

            // Crear un section para cada categoría y agregarlo como hermano del section original
            Object.keys(groupedItems).forEach(category => {
                const categoryItems = groupedItems[category];
                const sectionHtml = `
                    <section class="client-menu-section">
                        <h2>${category}</h2>
                        ${categoryItems.map((item, index) => `
                            <article>
                                <head>
                                    <h2>${item.name}</h2>
                                    <p>Calificación <span class="rating">${item.rating}/5</span></p> 
                                    <a href="#" onclick="alert('comentarios')" class="btn btn-primary">Ver comentarios</a>
                                </head>
                                <div>
                                    <img src="${imageUrls[index]}" alt="Imagen de la comida">
                                    <h3>Descripción</h3>
                                    <p>${item.description}</p>
                                </div>
                                <footer>
                                    <input type="number" min="1" max="99" value="1" class="quantity-input">
                                    <button class="btn btn-primary" data-id="${item.id}">Añadir</button>
                                </footer>
                            </article>
                        `).join('')}
                    </section>
                `;
                this.menuSection.insertAdjacentHTML('afterend', sectionHtml);
            });

            // Add event listeners to "Añadir" buttons
            document.querySelectorAll('.client-menu-section .btn.btn-primary').forEach(button => {
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