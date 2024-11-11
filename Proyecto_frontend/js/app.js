import { routerInstance } from './router.js';
import authService from './authService.js';
import orderService from './orderService.js';
import menuService from './menuService.js';
import notificationService from './notificationService.js';
import checkoutService from './checkoutService.js';
import reviewService from './reviewService.js';
import './customCode.js'; 
import cart from './cart.js';

document.addEventListener("DOMContentLoaded", () => {
    // Inicializar la aplicación
    authService.init();
    orderService.init();
    menuService.init();
    notificationService.init();
    checkoutService.init();
    reviewService.init();
    cart.init();
    routerInstance.router();
});

