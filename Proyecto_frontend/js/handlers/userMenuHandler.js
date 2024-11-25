import menuService from '../menuService.js';
import { routerInstance } from '../router.js';
import cart from '../cart.js';
import authService from '../authService.js';
import reviewsService from '../reviewService.js';   

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
            const newModalCart = modalCart.cloneNode(true);
            modalCart.parentNode.replaceChild(newModalCart, modalCart);
            newModalCart.addEventListener('click', (event) => {
                const menuAddEditAdmin = document.getElementById('modal-cart');
                if (menuAddEditAdmin) {
                    menuAddEditAdmin.style.display = 'none';
                }
            });
        }
        
        const modalButton = document.getElementById('cart-button');
        if (modalButton) {
            const newModalButton = modalButton.cloneNode(true);
            modalButton.parentNode.replaceChild(newModalButton, modalButton);
            newModalButton.addEventListener('click', (event) => {
                const menuAddEditAdmin = document.getElementById('modal-cart');
                if (menuAddEditAdmin) {
                    menuAddEditAdmin.style.display = 'block';
                    menuAddEditAdmin.scrollIntoView({ behavior: 'smooth' });
                }
            });
        }
    }

    getStarRatingHtml(rating) {
        // Convertir el rating a número
        rating = parseFloat(rating);
        const fullStars = Math.floor(rating);
        const halfStar = rating % 1 >= 0.5 ? 1 : 0;
        const emptyStars = 5 - fullStars - halfStar;
        console.log('Rating:', rating, 'Full stars:', fullStars, 'Half star:', halfStar, 'Empty stars:', emptyStars);
        return `
            ${'<span class="star full">★</span>'.repeat(fullStars)}${halfStar ? '<span class="star half">★</span>' : ''}${'<span class="star empty">☆</span>'.repeat(emptyStars)}
        `.trim();
    }

    async showComments(itemId) {
        try {
            const reviews = await reviewsService.getReviewById(itemId);
            console.log('Reviews:', reviews);
            const comments = reviews.reviews || [];
            const commentsHtml = comments.map(comment => `
                <div class="comment">
                    <p>${this.getStarRatingHtml(comment.rating)}</p>
                    <p><em>${new Date(comment.created_at).toLocaleDateString()}</em></p>
                    <p>${comment.comment}</p>
                </div>
            `).join('');
    
            const modalHtml = `
                <div class="modal" id="comments-modal">
                    <div class="modal-content">
                        <span class="close" id="close-comments-modal">&times;</span>
                        <h2>Comentarios</h2>
                        ${commentsHtml}
                    </div>
                </div>
            `;
    
            document.body.insertAdjacentHTML('beforeend', modalHtml);
    
            const modal = document.getElementById('comments-modal');
            const closeModal = document.getElementById('close-comments-modal');
    
            modal.style.display = 'block';
    
            closeModal.onclick = () => {
                modal.style.display = 'none';
                modal.remove();
            };
    
            window.onclick = (event) => {
                if (event.target == modal) {
                    modal.style.display = 'none';
                    modal.remove();
                }
            };
        } catch (error) {
            console.error('Error fetching comments:', error);
        }
    }

    async renderMenu(menuItems) {
        console.log('renderMenu called');

        this.menuSection = document.querySelector('.client-menu-section-first');
        if (this.menuSection) {
            const categoriesResponse = await menuService.getCategories();
            const categories = categoriesResponse.data;
    
            // Crear un mapa de categorías para un acceso rápido
            const categoryMap = {};
            if (Array.isArray(categories)) {
                categories.forEach((category) => {
                    categoryMap[category.id] = category.name;
                });
            }

            //cremaois un mapa de reseñas consultando para cada item del menu
            const reviewsMap = {};
            for (const item of menuItems) {
                const reviews = await reviewsService.getReviewById(item.id);
                console.log('Reviews:', reviews);
                if(parseInt(reviews.count) > 0){
                    reviewsMap[item.id] = reviews.average ;
                }else{
                    reviewsMap[item.id] = 5;
                }   
            }

            console.log('MAP:', reviewsMap);

    
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
                                    <p>Calificación <span class="rating">${this.getStarRatingHtml(reviewsMap[item.id])}</span></p>
                                     <span class="view-comments" data-id="${item.id}">Ver comentarios</span>
                                </head>
                                <div>
                                    <img src="" alt="Imagen de la comida" class="menu-item-image" data-photo="${item.photo}">
                                    <h3>Descripción</h3>
                                    <p>${item.description}</p>
                                    <span class='price-container'>Precio: $${item.price}</span>
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

            // Add event listeners to "Ver comentarios" buttons
            document.querySelectorAll('.client-menu-section .view-comments').forEach(button => {
                button.addEventListener('click', async (event) => {
                    event.preventDefault();
                    const itemId = event.target.getAttribute('data-id');
                    await this.showComments(itemId);
                });
            });
    
            // Add event listeners to "Añadir" buttons
            document.querySelectorAll('.client-menu-section .btn.btn-primary').forEach(button => {
                button.addEventListener('click', async (event) => {
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
                        await cart.addItem(item);
                    }
                });
            });
        }
    }
}

export default UserMenuHandler;