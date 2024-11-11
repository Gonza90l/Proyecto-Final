import authService from './authService.js';
import menuService from './menuService.js';

class Cart {
    constructor() {
        this.items = [];
    }

    init() {
        this.loadCart();
    }

    addItem(item) {
        const existingItem = this.items.find(i => i.id === item.id);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            item.quantity = 1;
            this.items.push(item);
        }
        this.saveCart();
    }

    removeItem(itemId) {
        const itemIndex = this.items.findIndex(item => item.id === itemId);
        if (itemIndex > -1) {
            if (this.items[itemIndex].quantity > 1) {
                this.items[itemIndex].quantity -= 1;
            } else {
                this.items.splice(itemIndex, 1);
            }
        }
        this.saveCart();
    }

    getTotal() {
        return this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
    }

    getItems() {
        return this.items;
    }

    clearCart() {
        this.items = [];
        this.saveCart();
    }

    getItemQuantity(itemId) {
        const item = this.items.find(item => item.id === itemId);
        return item ? item.quantity : 0;
    }

    saveCart() {
        localStorage.setItem('cart', JSON.stringify(this.items));
        this.renderCart();
    }

    loadCart() {
        const savedCart = localStorage.getItem('cart');
        this.items = savedCart ? JSON.parse(savedCart) : [];
        this.renderCart();
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
                        <td>${item.name}</td>
                        <td>${item.quantity}</td>
                        <td>${item.price}</td>
                        <td>${item.price * item.quantity}</td>
                        <td><button class="cart-item-remove" data-id="${item.id}">+</button><button class="cart-item-remove" data-id="${item.id}">-</button></td>
                    `;
                    cartItemsContainer.appendChild(cartItemRow);
                    // si no hay imagen o no se puede cargar, se muestra una imagen por defecto
                    cartItemRow.querySelector('img').onerror = () => cartItemRow.querySelector('img').src = 'img/plato-home.jpg';
                }
    
                const cartTotal = this.items.reduce((total, item) => total + (item.price * item.quantity), 0);
                document.getElementById('cart-total').textContent = cartTotal;
            }
        }
    }
}

const cart = new Cart();
export default cart;