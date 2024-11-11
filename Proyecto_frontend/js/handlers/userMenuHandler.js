import menuService from '../menuService.js';
import { routerInstance } from '../router.js';
import cart from '../cart.js';
import authService from '../authService.js';

class UserMenuHandler {

    constructor() {
        console.log('UserMenuHandler instance created');
    }

    async init() {
        console.log('UserMenuHandler initialized');
        this.loadMenus();
        this.configureButtons();
    }

    async loadMenus() {
        console.log('loadMenus called');
        if(await authService.isAuthenticated()){
            try {
                const menuItems = await menuService.getAllMenuItems();
                this.renderMenu(menuItems.data);
            } catch (error) {
                console.error('Error fetching menu items:', error);
            }
        }
    }

    configureButtons() {
        console.log('configureButtons called');
        const modalCart = document.getElementById('close-modal-cart');
        if (modalCart) {
            modalCart.addEventListener('click', (event) => {
                const menuAddEditAdmin = document.getElementById('modal-cart');
                if (menuAddEditAdmin) {
                    menuAddEditAdmin.style.display = 'none';
                }
            });
        }
        
        const modalButton= document.getElementById('cart-button');
        if (modalButton) {
            modalButton.addEventListener('click', (event) => {
                const menuAddEditAdmin = document.getElementById('modal-cart');
                if (menuAddEditAdmin) {
                    menuAddEditAdmin.style.display = 'block';
                    menuAddEditAdmin.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }
    }

    async renderMenu(menuItems) {
        console.log('renderMenu called');

        this.menuSection = document.querySelector('.client-menu-section-first');
        if (this.menuSection) {
            const categoriesResponse = await menuService.getCategories();
            const categories = categoriesResponse.data;
            console.log('>>>>>Categories:', categories);
    
            // Crear un mapa de categorías para un acceso rápido
            const categoryMap = {};
            if (Array.isArray(categories)) {
                categories.forEach((category) => {
                    categoryMap[category.id] = category.name;
                });
            }
    
            // Agrupar los elementos del menú por categoría
            const groupedItems = menuItems.reduce((groups, item) => {
                const category = categoryMap[item.category_id] || 'Sin categoría';
                if (!groups[category]) {
                    groups[category] = [];
                }
                groups[category].push(item);
                return groups;
            }, {});

    
            // Crear un section para cada categoría y agregarlo como hermano del section original
            for (const category in groupedItems) {
                console.log('Category:', category);
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
                                    <img src="" alt="Imagen de la comida" class="menu-item-image" data-photo="${item.photo}">
                                    <h3>Descripción</h3>
                                    <p>${item.description}</p>
                                </div>
                                <footer>
                                    <input type="number" min="1" max="99" value="1" class="quantity-input">
                                    <button  class="btn btn-primary" data-id="${item.id}">Añadir</button>
                                </footer>
                            </article>
                        `).join('')}
                    </section>
                `;
                this.menuSection.insertAdjacentHTML('afterend', sectionHtml);
            }
    
            // Obtener las URLs de las imágenes y asignarlas a los elementos correspondientes
            const imageElements = document.querySelectorAll('.menu-item-image');
            for (const imgElement of imageElements) {
                const photo = imgElement.getAttribute('data-photo');
                const imageUrl = await menuService.getImagefromServer(photo);
                imgElement.src = imageUrl;
            }
    
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