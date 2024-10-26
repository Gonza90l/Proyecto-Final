import { routeConfig } from './routes.js';

const routes = {};
const protectedRoutes = new Set();
const roleBasedRoutes = {}; // Rutas basadas en roles
const fragmentCache = {};

// Registrar rutas en base a configuración
routeConfig.forEach(({ path, view, protected: isProtected, role }) => {
    registerRoute(path, view, isProtected, role);
});

function registerRoute(path, view, isProtected = false, role = null) {
    routes[path] = { view, role };
    if (isProtected) protectedRoutes.add(path);
    if (role) roleBasedRoutes[path] = role;
}

// Función para verificar autenticación
async function isAuthenticated() {
    return true
    try {
        return await authService.isAuthenticated();
    } catch (err) {
        console.error('Error checking authentication:', err);
        return false;
    }
}

// Función para obtener el rol del usuario
async function getRole() {
    return 'user';
    try {
        return await authService.getRole();
    } catch (err) {
        console.error('Error fetching user role:', err);
        return null;
    }
}

// Router principal
export async function router() {
    const path = window.location.pathname;
    const route = routes[path] || routes['/404'];
    const authenticated = await isAuthenticated();

    if (protectedRoutes.has(path)) {
        if (!authenticated) {
            redirectToLogin();
            return;
        }

        const userRole = await getRole();
        if (route.role && route.role !== userRole) {
            // Si el usuario no tiene el rol correcto, redirigir a acceso denegado o dashboard
            redirectToDashboard(userRole);
            return;
        }
    }

    // Si el usuario está autenticado y accede a login o registro, redirigir al dashboard
    if (authenticated && ['/','/login','/register'].includes(path)) {
        const userRole = await getRole();
        redirectToDashboard(userRole);
        return;
    }

    loadView(route.view);
}

// Cargar una vista
async function loadView(route) {
    try {
        const response = await fetch(route);
        if (!response.ok) throw new Error('Vista no generada para esta ruta.');
        const html = await response.text();
        document.getElementById('app').innerHTML = html;
    } catch (err) {
        console.error('Error loading view:', err);
        showError('Error al cargar la vista.');
    }
}

// Redirigir a login
function redirectToLogin() {
    window.history.pushState({}, '', '/login');
    loadView(routes['/login'].view);
}

// Redirigir al dashboard adecuado según el rol
function redirectToDashboard(userRole) {
    if (userRole === 'admin') {
        window.history.pushState({}, '', '/admin-dashboard');
        loadView(routes['/admin-dashboard'].view);
    } else {
        window.history.pushState({}, '', '/dashboard');
        loadView(routes['/dashboard'].view);
    }
}

// Cargar fragmentos HTML y almacenarlos en caché
async function loadFragments() {
    const fragments = document.querySelectorAll('[data-fragment]');
    await Promise.all([...fragments].map(async (fragment) => {
        const fragmentName = fragment.getAttribute('data-fragment');
        const url = `./views/fragments/${fragmentName}.html`;

        try {
            if (!fragmentCache[fragmentName]) {
                console.log(`Loading fragment from ${url}`);
                const response = await fetch(url);
                if (!response.ok) throw new Error(`No se pudo cargar ${fragmentName}`);
                fragmentCache[fragmentName] = await response.text();
            }
            fragment.innerHTML = fragmentCache[fragmentName];
        } catch (err) {
            console.error(`Error loading fragment: ${fragmentName}`, err);
            fragment.innerHTML = '<p>Error al cargar fragmento.</p>';
        }
    }));
}

// Mostrar un mensaje de error
function showError(message) {
    document.getElementById('app').innerHTML = `<div class="error">${message}</div>`;
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

// Cargar fragmentos al inicio
document.addEventListener('DOMContentLoaded', loadFragments);
