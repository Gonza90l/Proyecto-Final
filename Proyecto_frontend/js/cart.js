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
        this.renderCart();
    }

    loadCart() {
        const savedCart = localStorage.getItem('cart');
        this.items = savedCart ? JSON.parse(savedCart) : [];
        this.renderCart();
    }

    renderCart(){
        //localizamos si existe el boton del carrito para actualizar el numero de items por ID
        const cartButton = document.getElementById('cart-button');  
        const itemCount = document.getElementById('item-count');
        if(itemCount){
            itemCount.innerHTML = this.items.length;
        }
        //si noo hay articulos en el carrito, ocultamos el boton
        if(this.items.length === 0){
            if(cartButton){
                cartButton.style.display = 'none';
            }
        }
    }

}

const cart = new Cart();

export default cart;