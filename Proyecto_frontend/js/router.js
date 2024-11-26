import { routeConfig } from './routes.js';
import authService from './authService.js';
import cart from './cart.js';

class Router {
    constructor() {
        this.routes = {};
        this.protectedRoutes = new Set();
        this.roleBasedRoutes = {}; // Rutas basadas en roles
        this.fragmentCache = {};
        this.onViewLoaded = null; // Callback para ejecutar después de cargar la vista
        this.isRouting = false; // Flag to prevent multiple executions

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
        document.addEventListener('DOMContentLoaded', this.router.bind(this));
    }

    registerRoute(path, view, isProtected = false, role = null) {
        this.routes[path] = { view, role };
        if (isProtected) this.protectedRoutes.add(path);
        if (role) this.roleBasedRoutes[path] = role;
    }

    async isAuthenticated() {
        //marcamos el tiempo en que se ejecuta la funcion
        try {
            return await authService.isAuthenticated();
        } catch (err) {
            return false;
        }
    }

    async getRole() {
        try {
            return await authService.getRole();
        } catch (err) {
            console.error('Error fetching user role:', err);
            return null;
        }
    }

    async navigate(path, params = {}) {
        const url = new URL(window.location.origin + path);
        Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));
    
        if (this.routes[path]) {
            window.history.pushState({}, '', url);
            await this.router();
        }
    }

    async showNotification(message, type = 'info', duration = 3000) {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerText = message;
        document.body.appendChild(notification);
    
        setTimeout(() => {
            notification.classList.add('fade-out');
            notification.addEventListener('transitionend', () => {
                notification.remove();
            });
        }, duration);
    }

    async router() {
        if (this.isRouting) return; // Prevent multiple executions
        this.isRouting = true;

        const path = window.location.pathname;
        const route = this.routes[path] || this.routes['/404'];

        this.showLoading(); // Mostrar el elemento de carga

        const authenticated = await this.isAuthenticated();

        if (this.protectedRoutes.has(path)) {
            if (!authenticated) {
                this.redirectToLogin();
                this.isRouting = false;
                return;
            }

            const userRole = await this.getRole();
            if (route.role && route.role !== userRole) {
                this.redirectToDashboard(userRole);
                this.isRouting = false;
                return;
            }
        }

        if (authenticated && ['/','/login','/register'].includes(path)) {
            const userRole = await this.getRole();
            this.redirectToDashboard(userRole);
            this.isRouting = false;
            return;
        }

        await this.loadView(route.view + '?_=' + new Date().getTime());
        await cart.renderCart();
        
        this.hideLoading(); // Ocultar el elemento de carga
        this.isRouting = false;
    }

    async loadView(route) {
        try {
            if (!route) {
                throw new Error('Ruta no definida.');
            }
    
            const response = await fetch(route);
            if (!response.ok) throw new Error('Vista no generada para esta ruta.');
    
            const html = await response.text();
    
            if (html.includes('<title>Sistema para pedidos de comidas</title>')) {
                throw new Error('Vista no encontrada, asegúrate de que la vista existe y está en la carpeta correcta.');
            }
    
            const appElement = document.getElementById('app');
    
            if (!appElement) {
                throw new Error('Elemento con ID "app" no encontrado, asegúrate de que tu HTML tiene un elemento con ID "app".');
            }
    
            appElement.innerHTML = html;

            await this.loadFragments();

            if (this.onViewLoaded) {
                this.onViewLoaded();
            }
        } catch (err) {
            console.error('Error loading view:', err);
            this.showError(`Error al cargar la vista: ${err.message}`);
        }
    }

    redirectToLogin() {
        window.history.pushState({}, '', '/login');
        this.loadView(this.routes['/login'].view + '?_=' + new Date().getTime());
        this.hideLoading(); // Ocultar el elemento de carga
    }

    redirectToDashboard(userRole) {
        if (userRole === 'admin') {
            window.history.pushState({}, '', '/admin-dashboard');
            this.loadView(this.routes['/admin-dashboard'].view + '?_=' + new Date().getTime());
        } else {
            window.history.pushState({}, '', '/dashboard');
            this.loadView(this.routes['/dashboard'].view  + '?_=' + new Date().getTime());
        }
        this.hideLoading(); // Ocultar el elemento de carga
    }

    async loadFragments() {
        const fragments = document.querySelectorAll('[data-fragment]');
        await Promise.all([...fragments].map(async (fragment) => {
            const fragmentName = fragment.getAttribute('data-fragment');
            const url = `./views/fragments/${fragmentName}.html?_=${new Date().getTime()}`;
    
            try {
                if (!this.fragmentCache[fragmentName]) {
                    const response = await fetch(url);
                    if (!response.ok) throw new Error(`No se pudo cargar ${fragmentName}`);
                    
                    const html = await response.text();
    
                    if (html.includes('<title>Sistema para pedidos de comidas</title>')) {
                        throw new Error('Fragmento no encontrado, asegúrate de que el fragmento existe y está en la carpeta correcta.');
                    }
    
                    this.fragmentCache[fragmentName] = html;
                }
                fragment.innerHTML = this.fragmentCache[fragmentName];
            } catch (err) {
                console.error(`Error loading fragment: ${fragmentName}`, err);
                fragment.innerHTML = `
                    <div class="error-fragment">
                        <h2>Fragmento no encontrado</h2>
                        <p>Lo sentimos, el fragmento "${fragmentName}" no se pudo cargar.</p>
                    </div>
                `;
            }
        }));
    }

    showLoading() {
        const loadingElement = document.createElement('div');
        loadingElement.className = 'loading-overlay';
        loadingElement.innerHTML = `
            <div class="spinner"></div>
        `;
        document.body.appendChild(loadingElement);
    }

    hideLoading() {
        const loadingElement = document.querySelector('.loading-overlay');
        if (loadingElement) {
            loadingElement.remove();
        }
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

export const routerInstance = new Router();