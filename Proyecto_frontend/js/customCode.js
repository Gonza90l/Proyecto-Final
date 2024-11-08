// CustomCode.js
// Aqui se declara todo el código accesorio que se necesita para que la aplicación funcione correctamente. Este archivo no se debe modificar.
import authService from './authService.js';
import { routerInstance } from './router.js';
import menuService from './menuService.js';
import AdminMenuHandler from './handlers/adminMenuHandler.js';
import LoginHandler from './handlers/loginHandler.js';


routerInstance.onViewLoaded = async () => {
    console.log('onViewLoaded function executed');
    // ***************************************************************************************
    // Código que se ejecutará después de que el router haya cargado completamente las vistas
    // Aquí agregar el código que necesites ejecutar una vez que la vista se haya cargado
    // por ejemplo asignacion de manejadores de eventos, inicialización de componentes, etc.
    // ***************************************************************************************

    // Inicializar el manejador de eventos de login / reguistro
    const loginHandler = new LoginHandler();
    loginHandler.init();

    // Inicializar el manejador de eventos del menú de administración
    const adminMenuHandler = new AdminMenuHandler();
    await adminMenuHandler.init();

    const gotoorigin404 = document.getElementById('404-go-to-origin');
    if (gotoorigin404) {
        gotoorigin404.addEventListener('click', function() {
            window.history.pushState({}, '', '/');
            routerInstance.router()
        });
    }

};

//*******************************************************************************************
// Codigo general que se ejecutará en todas las vistas de la aplicación
// Permite incorporar funciones que se necesiten
// ***************************************************************************************




