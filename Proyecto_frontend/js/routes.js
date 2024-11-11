// routes.js
// Acá se define la configuración de las rutas de la aplicación. 
//Cada ruta tiene un path, una vista asociada y puede ser protegida o no. 
//Además, se puede especificar un rol requerido para acceder a la ruta.

export const routeConfig = [
    { path: '/', view: '/views/home.html' },
    { path: '/menu', view: '/views/menu.html', protected: true, role: 'user' },
    { path: '/about', view: '/views/about.html' },
    { path: '/landing', view: '/views/landing.html' },
    { path: '/404', view: '/views/404.html' },
    { path: '/login', view: '/views/login.html' },
    { path: '/register', view: '/views/register.html' },
    { path: '/dashboard', view: '/views/user-dashboard.html', protected: true, role: 'user' }, // Dashboard para usuario regular
    { path: '/admin-dashboard', view: '/views/admin-dashboard.html', protected: true, role: 'admin' }, // Dashboard para admins
    { path: '/admin-menu', view: '/views/admin-menu.html', protected: true, role: 'admin' }, // Dashboard para admins
    { path: '/admin-orders', view: '/views/admin-orders.html', protected: true, role: 'admin' }, // Dashboard para admins
    { path: '/checkout', view: '/views/checkout.html' , protected: true, role: 'user' }
];