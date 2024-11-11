import authService from './authService.js';
import menuService from './menuService.js';

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

    }

    loadCart() {
        const savedCart = localStorage.getItem('cart');
        this.items = savedCart ? JSON.parse(savedCart) : [];

    }

    renderCart(){
        
    }

}

const cart = new Cart();

export default cart;