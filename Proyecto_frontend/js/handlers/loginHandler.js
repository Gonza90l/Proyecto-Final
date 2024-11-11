import authService from '../authService.js';
import { routerInstance } from '../router.js';

class LoginHandler {
    constructor() {
        this.loginForm = document.getElementById('login-form');
        this.logoutButton = document.getElementById('logout-button');
        this.registerForm = document.getElementById('register-form');
    }

    init() {
        this.setupLoginForm();
        this.setupLogoutButton();
        this.setupRegisterForm();
    }

    setupLoginForm() {
        if (this.loginForm) {
            this.loginForm.addEventListener('submit', (event) => {
                event.preventDefault();
                const formData = new FormData(this.loginForm);
                const email = formData.get('username');
                const password = formData.get('password');
                login(email, password);
            });
        }
    }

    setupLogoutButton() {
        if (this.logoutButton) {
            this.logoutButton.addEventListener('click', async () => {
                await authService.logout();
                window.history.pushState({}, '', '/login');
                routerInstance.router();
            });
        }
    }

    setupRegisterForm() {
        if (this.registerForm) {
            this.registerForm.addEventListener('submit', (event) => {
                event.preventDefault();
                const formData = new FormData(this.registerForm);
                const name = formData.get('name');
                const lastname = formData.get('lastname');
                const email = formData.get('email');
                const password = formData.get('password');
                register(name, lastname, email, password);
            });
        }
    }
}

//login, esta función se encarga de hacer el login del usuario
async function login(email, password) {
    routerInstance.showLoading();
    try {
        const isAuthenticated = await authService.login(email, password);
        if (isAuthenticated) {
            window.history.pushState({}, '', '/');
            routerInstance.router();
        } else {
            routerInstance.showNotification('Usuario o contraseña incorrectos', 'warning');
        }
    } catch (error) {
        routerInstance.showNotification('Error al iniciar sesión', 'error');
    }
    routerInstance.hideLoading();
}

//register, esta función se encarga de registrar un nuevo usuario
// todos los usuarios registrados serán de tipo "user"
// el Admin se crea durante la creación de la base de datos
async function register(name, lastname, email, password) {
    routerInstance.showLoading();
    try {
        const register = await authService.register(name, lastname, email, password);
        if (register.success) {
            window.history.pushState({}, '', '/login');
            routerInstance.router();
        } else {
            // si existe el campo error en la respuesta, lo devolvemos
            if (register.error) {
                alert('Error: ' + JSON.stringify(register.error));
            } else {
                alert('Error: Could not register user');
            }
        }
    } catch (error) {
        console.error('Register error:', error);
    }
    routerInstance.hideLoading();
}


export default LoginHandler;