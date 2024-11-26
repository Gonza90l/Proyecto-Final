import authService from './authService.js';
import CreateOrderRequestDto from './dtos/createOrderRequestDto.js';
import menuService from './menuService.js';
import orderService from './orderService.js';
import { routerInstance } from './router.js';

class Cart {
    constructor() {
        this.items = [];
    }

    init() {
        this.loadCart();
    }

    async createOrder() {
        //creamos el dto para enviar al backend
        //createOrderRequestDto.js
        const orderHasMenuDTO = this.items.map(item => ({ menu_id: item.id, quantity: item.quantity }));
        const userId = await authService.getUserId();
        if (!userId) {
            routerInstance.showNotification('Error al obtener el usuario', 'error');
            return null;
        }
        const createOrderRequestDto = new CreateOrderRequestDto(userId, this.getTotal(), 'CREATED', orderHasMenuDTO);
        const response = orderService.createOrder(createOrderRequestDto);
        if (response) {
            this.clearCart();
            return response;
        } else {
            return null;
        }
    }

    async addItem(item) {
        const existingItem = this.items.find(i => i.id === item.id);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            item.quantity = 1;
            this.items.push(item);
        }
        routerInstance.showNotification('Producto añadido al carrito', 'info');
        await this.saveCart(); // Cambiar a await para asegurar que el carrito se guarde antes de renderizar
    }

    async removeItem(itemId) {
        const itemIndex = this.items.findIndex(item => item.id == itemId);
        if (itemIndex > -1) {
            if (this.items[itemIndex].quantity > 1) {
                this.items[itemIndex].quantity -= 1;
            } else {
                this.items.splice(itemIndex, 1);
            }
        }
        await this.saveCart();
    }

    getTotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    getItems() {
        return this.items;
    }

    async clearCart() {
        this.items = [];
        await this.saveCart();
    }

    getItemQuantity(itemId) {
        const item = this.items.find(item => item.id === itemId);
        return item ? item.quantity : 0;
    }

    async saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.items));
        await this.renderCart();
    }

    async loadCart() {
        const savedCart = localStorage.getItem('cart');
        this.items = savedCart ? JSON.parse(savedCart) : [];
        await this.renderCart();
    }

    async renderCart() {
        const cartButton = document.getElementById('cart-button');
        const itemCount = document.getElementById('item-count');
        if (itemCount) {
            itemCount.innerHTML = this.items.reduce((count, item) => count + item.quantity, 0);
        }
    
        const cartModal = document.getElementById('modal-cart');
        if (cartModal) {
            const cartItemsContainer = cartModal.querySelector('tbody');
            if (cartItemsContainer) {
                cartItemsContainer.innerHTML = ''; // Clear existing items
    
                for (const item of this.items) {
                    const cartItemRow = document.createElement('tr');
                    const photo = await menuService.getImagefromServer(item.photo);
                    cartItemRow.innerHTML = `
                        <td><img src="${photo}" alt="${item.name}" class="cart-item-photo"></td>
                        <td class="cart-item-name">${item.name}</td>
                        <td class="cart-item-quantity">${item.quantity}</td>
                        <td class="cart-item-price">${item.price}</td>
                        <td class="cart-item-total">${item.price * item.quantity}</td>
                        <td class="cart-item-actions"><button class="cart-item-add" data-id="${item.id}">+</button><button class="cart-item-remove" data-id="${item.id}">-</button></td>
                    `;
                    cartItemsContainer.appendChild(cartItemRow);
                    // si no hay imagen o no se puede cargar, se muestra una imagen por defecto
                    cartItemRow.querySelector('img').onerror = () => cartItemRow.querySelector('img').src = 'img/plato-home.jpg';
                }
    
                const cartTotal = this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
                document.getElementById('cart-total').textContent = cartTotal;
    
                // Remove existing event listeners
                document.querySelectorAll('.cart-item-add').forEach(button => {
                    const newButton = button.cloneNode(true);
                    button.parentNode.replaceChild(newButton, button);
                });
    
                document.querySelectorAll('.cart-item-remove').forEach(button => {
                    const newButton = button.cloneNode(true);
                    button.parentNode.replaceChild(newButton, button);
                });
    
                // Agregar eventos a los botones de añadir y remover
                document.querySelectorAll('.cart-item-add').forEach(button => {
                    button.addEventListener('click', (event) => {
                        const itemId = event.target.getAttribute('data-id');
                        const item = this.items.find(item => item.id == itemId);
                        if (item) {
                            this.addItem(item);
                        }
                    });
                });
    
                document.querySelectorAll('.cart-item-remove').forEach(button => {
                    button.addEventListener('click', (event) => {
                        const itemId = event.target.getAttribute('data-id');
                        this.removeItem(itemId);
                    });
                });
    
                //si no existe el boton de checkout, no se añade el evento
                const checkoutButton = document.getElementById('checkout-button');
                if (checkoutButton) {
                    checkoutButton.onclick = async () => {
                        if (authService.isAuthenticated()) {
                            const order = {
                                items: this.items.map(item => ({ id: item.id, quantity: item.quantity })),
                                total: cartTotal
                            };
                            routerInstance.showNotification('Creando pedido...Espere...', 'info');
                            const orderId = await this.createOrder(order);
                            if (orderId) {
                                this.clearCart();
                                routerInstance.navigate('/checkout', { order: JSON.stringify(orderId) });
                            } else {
                                routerInstance.showNotification('Error al crear el pedido', 'error');
                            }
                        } else {
                            alert('Debes iniciar sesión para realizar un pedido');
                        }
                    };
                }
    
                if (this.items.length === 0) {
                    checkoutButton.style.display = 'none';
                } else {
                    checkoutButton.style.display = 'inline';
                }
            }
        }
    }

}

const cart = new Cart();
export default cart;