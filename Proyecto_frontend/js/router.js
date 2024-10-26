import { routeConfig } from './routes.js';
import authService from './authService.js';

class Router {
    constructor() {
        this.routes = {};
        this.protectedRoutes = new Set();
        this.roleBasedRoutes = {}; // Rutas basadas en roles
        this.fragmentCache = {};

        // Registrar rutas en base a configuración
        routeConfig.forEach(({ path, view, protected: isProtected, role }) => {
            this.registerRoute(path, view, isProtected, role);
        });

        // Manejar cambios en la URL
        window.onpopstate = this.router.bind(this);

        document.addEventListener('click', (event) => {
            if (event.target.tagName === 'A' && event.target.href.startsWith(window.location.origin)) {
                event.preventDefault();
                window.history.pushState({}, '', event.target.href);
                this.router();
            }
        });

        // Cargar fragmentos al inicio
        document.addEventListener('DOMContentLoaded', this.loadFragments.bind(this));
    }

    registerRoute(path, view, isProtected = false, role = null) {
        this.routes[path] = { view, role };
        if (isProtected) this.protectedRoutes.add(path);
        if (role) this.roleBasedRoutes[path] = role;
    }

    async isAuthenticated() {
        return true;
        try {
            return await authService.isAuthenticated();
        } catch (err) {
            console.error('Error checking authentication:', err);
            return false;
        }
    }

    async getRole() {
        return 'admin';
        try {
            return await authService.getRole();
        } catch (err) {
            console.error('Error fetching user role:', err);
            return null;
        }
    }

    async router() {
        const path = window.location.pathname;
        const route = this.routes[path] || this.routes['/404'];
        const authenticated = await this.isAuthenticated();

        if (this.protectedRoutes.has(path)) {
            if (!authenticated) {
                this.redirectToLogin();
                return;
            }

            const userRole = await this.getRole();
            if (route.role && route.role !== userRole) {
                // Si el usuario no tiene el rol correcto, redirigir a acceso denegado o dashboard
                this.redirectToDashboard(userRole);
                return;
            }
        }

        // Si el usuario está autenticado y accede a login o registro, redirigir al dashboard
        if (authenticated && ['/','/login','/register'].includes(path)) {
            const userRole = await this.getRole();
            this.redirectToDashboard(userRole);
            return;
        }

        this.loadView(route.view);
    }

    async loadView(route) {
        try {
            // Verificar si la ruta existe
            if (!route) {
                throw new Error('Ruta no definida.');
            }
    
            const response = await fetch(route);
            if (!response.ok) throw new Error('Vista no generada para esta ruta.');
    
            const html = await response.text();
    
            // Verificar si la respuesta es una página de error genérica
            if (html.includes('<title>Sistema para pedidos de comidas</title>')) {
                throw new Error('Vista no encontrada, asegúrate de que la vista existe y está en la carpeta correcta.');
            }
    
            const appElement = document.getElementById('app');
    
            if (!appElement) {
                throw new Error('Elemento con ID "app" no encontrado, asegúrate de que tu HTML tiene un elemento con ID "app".');
            }
    
            appElement.innerHTML = html;
        } catch (err) {
            console.error('Error loading view:', err);
            this.showError(`Error al cargar la vista: ${err.message}`);
        }
    }

    redirectToLogin() {
        window.history.pushState({}, '', '/login');
        this.loadView(this.routes['/login'].view);
    }

    redirectToDashboard(userRole) {
        if (userRole === 'admin') {
            window.history.pushState({}, '', '/admin-dashboard');
            this.loadView(this.routes['/admin-dashboard'].view);
        } else {
            window.history.pushState({}, '', '/dashboard');
            this.loadView(this.routes['/dashboard'].view);
        }
    }

    async loadFragments() {
        const fragments = document.querySelectorAll('[data-fragment]');
        await Promise.all([...fragments].map(async (fragment) => {
            const fragmentName = fragment.getAttribute('data-fragment');
            const url = `./views/fragments/${fragmentName}.html`;

            try {
                if (!this.fragmentCache[fragmentName]) {
                    console.log(`Loading fragment from ${url}`);
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`No se pudo cargar ${fragmentName}`);
                    this.fragmentCache[fragmentName] = await response.text();
                }
                fragment.innerHTML = this.fragmentCache[fragmentName];
            } catch (err) {
                console.error(`Error loading fragment: ${fragmentName}`, err);
                fragment.innerHTML = '<p>Error al cargar fragmento.</p>';
            }
        }));
    }

    showError(message) {
        document.body.innerHTML = `
        <div class="error-container">
            <div class="error-content">
                <h1>Error</h1>
                <p>${message}</p>
                <button onclick="window.location.href='/'">Volver al inicio</button>
            </div>
        </div>
    `;
    }
}

// Exportar una instancia de la clase Router
export const routerInstance = new Router();