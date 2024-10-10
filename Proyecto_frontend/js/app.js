import { router } from './router.js';
import { authService } from './authService.js';

document.addEventListener("DOMContentLoaded", () => {
    // Inicializar la aplicación
    authService.init();
    router();
});
