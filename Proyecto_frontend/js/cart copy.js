import authService from './authService.js';
import menuService from './menuService.js';

class Cart {
    constructor() {
        
    }

    init () {
        this.loadCart();
    }

    addItem(item) {
        console.log(">>>>", item)
        this.items.push(item);
        this.saveCart();
    }

    removeItem(itemId) {
        console.log("????",itemId);
        this.items = this.items.filter(item => item.id != itemId);
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
        localStorage.setItem('cart', JSON.stringify(this.items));
        this.renderCart()
    }

    loadCart() {
        const savedCart = localStorage.getItem('cart');
        this.items = savedCart ? JSON.parse(savedCart) : [];
        this.renderCart()
    }

    // renderizamoos un boton de carrito flotante
    async renderCartButton() {
        console.log('renderCartButton');
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
                this.showCart();
            });
            document.body.appendChild(cartButton);
        } else {
            existingCartButton.querySelector('.item-count').textContent = this.items.length;
        }
    }

    // renderizamos el carrito en una ventana modal
    renderCart() {
        this.renderCartButton();
        if(this.items.length === 0) {
            const cartModal = document.querySelector('.cart-modal');
            if (cartModal) {
                cartModal.display = 'none';
            }
        }
    }

    showCart() {
        const cartModal = document.querySelector('.cart-modal');
    
        const modal = document.createElement('div');
        modal.classList.add('cart-modal');
        modal.innerHTML = `
            <div class="cart-content">
                <h2>Carrito</h2>
                <ul>
                    ${this.items.map(item => item ? `
                        <li>
                            <span>${item.name}</span>
                            <span>${item.price}</span>
                            <button class="btn-remove" data-id="${item.id}">Eliminar</button>
                        </li>
                    ` : '').join('')}
                </ul>
                <p>Total: $${this.getTotal()}</p>
                <button class="btn btn-primary">Pagar</button>
            </div>
        `;
    
        modal.querySelector('.btn.btn-primary').addEventListener('click', () => {
            this.clearCart();
            this.renderCartButton();
            modal.remove();
        });
        
        modal.querySelectorAll('.cart-content li button').forEach(button => {
            button.addEventListener('click', (event) => {
                const itemId = event.target.getAttribute('data-id');
                this.removeItem(itemId);
                this.renderCart();
                console.log('Removed item from cart:', itemId);
            });
        });
    
        document.body.appendChild(modal);
    }


}

const cart = new Cart();

export default cart;