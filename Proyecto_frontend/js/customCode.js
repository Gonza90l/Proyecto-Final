// CustomCode.js
// Aqui se declara todo el código accesorio que se necesita para que la aplicación funcione correctamente. Este archivo no se debe modificar.
import { routerInstance } from './router.js';
import AdminMenuHandler from './handlers/adminMenuHandler.js';
import LoginHandler from './handlers/loginHandler.js';
import UserMenuHandler from './handlers/userMenuHandler.js';
import CheckOutHandler from './handlers/checkoutHandler.js';
import UserDashboardHandler from './handlers/userDashboardHandler.js';
import AdminOrdersHandler from './handlers/adminOrdersHandler.js';
import authService from './authService.js';

routerInstance.onViewLoaded = async () => {
    console.log('onViewLoaded function executed');
    // ***************************************************************************************
    // Código que se ejecutará después de que el router haya cargado completamente las vistas
    // Aquí agregar el código que necesites ejecutar una vez que la vista se haya cargado
    // por ejemplo asignacion de manejadores de eventos, inicialización de componentes, etc.
    // ***************************************************************************************

    // Inicializar el manejador de eventos del menú de administración
    const adminMenuHandler = new AdminMenuHandler();
    await adminMenuHandler.init();

    // Inicializar el manejador de eventos del menú de usuario
    const userMenuHandler = new UserMenuHandler();
    userMenuHandler.init();

    // Inicializar el manejador de eventos de checkout
    const checkOutHandler = new CheckOutHandler();
    checkOutHandler.init();

    const userDashboardHandler = new UserDashboardHandler();
    userDashboardHandler.init();

    const adminOrdersHandler = new AdminOrdersHandler();
    adminOrdersHandler.init();

    const gotoorigin404 = document.getElementById('404-go-to-origin');
    if (gotoorigin404) {
        gotoorigin404.addEventListener('click', function() {
            window.history.pushState({}, '', '/');
            routerInstance.router()
        });
    }


     // Generamos la barra de navegación de acuerdo a si está logueado o no
     const navBar = document.getElementById('navigator');
     if (await authService.isAuthenticated()) {
         if (navBar) {
             if (await authService.getRole() === 'user') {
                 // Creamos el menú de usuario y lo renderizamos directamente desde JS
                 navBar.innerHTML = `
                 <ul>
                     <li><a onclick="navigate('/')" href="#" title="Mis Pedidos"><span class="material-icons" aria-label="Administrar Pedidos">list_alt</span><span class="fallback-text">Mis Pedidos</span></a></li>
                     <li><a onclick="navigate('/menu')" href="#" title="Menu"><span class="material-icons" aria-label="Administrar Menús">restaurant_menu</span><span class="fallback-text">Menú</span></a></li>
                     <li><a onclick="" href="#" title="Notifications"><span class="material-icons" aria-label="Notifications">notifications</span><span class="fallback-text">Notifications</span></a></li>
                     <li><a href="#" id="logout-button" title="Cerrar Sesión"><span class="material-icons" aria-label="Cerrar Sesión">logout</span><span class="fallback-text">Cerrar Sesión</span></a></li>
                 </ul>
                 `;
             } else {
                 // Creamos el menú de administrador y lo renderizamos directamente desde JS
                 navBar.innerHTML = `
                 <ul>
                     <li><a onclick="navigate('/admin-dashboard')" href="#" title="Dashboard"><span class="material-icons" aria-label="Dashboard">dashboard</span><span class="fallback-text">Dashboard</span></a></li>
                     <li><a onclick="navigate('/admin-menu')" href="#" title="Administrar Menús"><span class="material-icons" aria-label="Administrar Menús">restaurant_menu</span><span class="fallback-text">Administrar Menús</span></a></li>
                     <li><a onclick="navigate('/admin-orders')" href="#" title="Administrar Pedidos"><span class="material-icons" aria-label="Administrar Pedidos">list_alt</span><span class="fallback-text">Administrar Pedidos</span></a></li>
                     <li><a onclick="" href="#" title="Notifications"><span class="material-icons" aria-label="Notifications">notifications</span><span class="fallback-text">Notifications</span></a></li>
                     <li><a href="#" id="logout-button" title="Cerrar Sesión"><span class="material-icons" aria-label="Cerrar Sesión">logout</span><span class="fallback-text">Cerrar Sesión</span></a></li>
                 </ul>
                 `;
             }
         }
     } else {
         if (navBar) {
             navBar.innerHTML = `
             <ul>
                 <li><a onclick="navigate('/')" href="#" title="Home"><span class="material-icons" aria-label="Home">home</span><span class="fallback-text">Home</span></a></li>
                 <li><a onclick="navigate('/login')" href="#" title="Login"><span class="material-icons" aria-label="Login">login</span><span class="fallback-text">Login</span></a></li>
                 <li><a onclick="navigate('/register')" href="#" title="Register"><span class="material-icons" aria-label="Register">person_add</span><span class="fallback-text">Register</span></a></li>
             </ul>
             `;
         }
     }
 
     // Manejo del menú hamburguesa
     const menuToggle = document.getElementById('menu-toggle');
     const navigation = document.querySelector('.navigation');
     if (menuToggle && navigation) {
         menuToggle.addEventListener('click', () => {
             navigation.classList.toggle('active');
         });
     }

     // Inicializar el manejador de eventos de login / reguistro
     const loginHandler = new LoginHandler();
     loginHandler.init();


    // Hacer que navigate esté disponible globalmente
    window.navigate = routerInstance.navigate.bind(routerInstance);

    // Obtener el elemento con el id 'footerYear'
    const footerYearElement = document.getElementById('footerYear');
    // Verificar si el elemento existe
    if (footerYearElement) {
        // Obtener el año actual
        const currentYear = new Date().getFullYear();
        // Asignar el año actual al elemento
        footerYearElement.textContent = currentYear;
    }
    

}
//*******************************************************************************************
// Codigo general que se ejecutará en todas las vistas de la aplicación
// Permite incorporar funciones que se necesiten
// ***************************************************************************************
