import { ApiClient } from './apiClient.js';
import { authService } from './authService.js';

const routes = {
    '/': '/views/home.html',
    '/menu': '/views/menu.html',
    '/about': '/views/about.html',
    '/landing': '/views/landing.html',
    '/404': '/views/404.html',
    '/login': '/views/login.html',
    '/register': '/views/register.html',
    '/dashboard': '/views/dashboard.html' // Añadir la ruta del dashboard
};

const publicRoutes = ['/', '/about', '/landing', '/404', '/login', '/register'];

const apiClient = new ApiClient(window.location.origin);

async function isAuthenticated() {
    return await authService.isAuthenticated();
}

export async function router() {
    const path = window.location.pathname;
    const route = routes[path] || routes['/404'];

    const authenticated = await isAuthenticated();

    if (publicRoutes.includes(path)) {
        if (authenticated) {
            if (path === '/' || path === '/login' || path === '/register') {
                // Redirigir al dashboard si está autenticado y está en la página de home, login o registro
                window.history.pushState({}, '', '/dashboard');
                loadView(routes['/dashboard']);
                return;
            }
        }
    } else {
        if (!authenticated) {
            // Redirigir al login si no está autenticado y está intentando acceder a una ruta protegida
            window.history.pushState({}, '', '/login');
            loadView(routes['/login']);
            return;
        }
    }

    loadView(route);
}

function loadView(route) {
    apiClient.get(route)
        .then(html => {
            document.getElementById('app').innerHTML = html;
        })
        .catch(err => console.error('Error loading view:', err));
}

// Manejar cambios en la URL
window.onpopstate = router;

document.addEventListener('click', (event) => {
    if (event.target.tagName === 'A' && event.target.href.startsWith(window.location.origin)) {
        event.preventDefault();
        window.history.pushState({}, '', event.target.href);
        router();
    }
});