import authService from './authService.js';

class Cart {
    constructor() {
        
    }

    init () {
        this.loadCart();
    }

    addItem(item) {
        this.items.push(item);
        this.saveCart();
    }

    removeItem(itemId) {
        this.items = this.items.filter(item => item.id !== itemId);
        this.saveCart();
    }

    getTotal() {
        return this.items.reduce((total, item) => total + item.price, 0);
    }

    getItems() {
        return this.items;
    }

    clearCart() {
        this.items = [];
        this.saveCart();
    }

    saveCart() {
        this.renderCartButton()
        localStorage.setItem('cart', JSON.stringify(this.items));
    }

    loadCart() {
        const savedCart = localStorage.getItem('cart');
        this.items = savedCart ? JSON.parse(savedCart) : [];
        this.renderCartButton()
    }

    // renderizamoos un boton de carrito flotante
    async renderCartButton() {

        const existingCartButton = document.querySelector('.cart-button');

        if (! await authService.isAuthenticated()) {
            if (existingCartButton) {
                existingCartButton.remove();
                this.clearCart();
            }
            return;
        }
        

        if (this.items.length === 0) {
            if (existingCartButton) {
                existingCartButton.remove();
            }
            return;
        }
    
        if (!existingCartButton) {
            const cartButton = document.createElement('button');
            cartButton.classList.add('cart-button');
            cartButton.innerHTML = `
                <span class="material-icons">shopping_cart</span>
                <span class="item-count">${this.items.length}</span>
            `;
            cartButton.addEventListener('click', () => {
                this.renderCart();
            });
            document.body.appendChild(cartButton);
        } else {
            existingCartButton.querySelector('.item-count').textContent = this.items.length;
        }
    }

    // renderizamos el carrito en una ventana modal
    renderCart() {

    }


}

const cart = new Cart();

export default cart;