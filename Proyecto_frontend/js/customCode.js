// CustomCode.js
// Aqui se declara todo el código accesorio que se necesita para que la aplicación funcione correctamente. Este archivo no se debe modificar.
import authService from './authService.js';
import { routerInstance } from './router.js';
import menuService from './menuService.js';

routerInstance.onViewLoaded = () => {
    // ***************************************************************************************
    // Código que se ejecutará después de que el router haya cargado completamente las vistas
    // Aquí agregar el código que necesites ejecutar una vez que la vista se haya cargado
    // ***************************************************************************************

    //login agregar evento al formulario de login
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const formData = new FormData(loginForm);
            const email = formData.get('username');
            const password = formData.get('password');
            login(email, password);
        });
    }

    
    //logout agregar evento al botón de logout
    const logoutButton = document.getElementById('logout-button');
    if (logoutButton) {
        logoutButton.addEventListener('click', async () => {
            await authService.logout();
            window.history.pushState({}, '', '/login');
            routerInstance.router();
        });
    }

    //register agregar evento al formulario de registro
    const registerForm = document.getElementById('register-form');
    if (registerForm) {
        registerForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const formData = new FormData(registerForm);
            const name = formData.get('name');
            const lastname = formData.get('lastname');
            const email = formData.get('email');
            const password = formData.get('password');
            register(name, lastname, email, password);
        });
    }

<<<<<<< HEAD
    //addOrUpdateMenu agregar evento al formulario de agregar o actualizar menu
    const addOrUpdateMenuForm = document.getElementById('addOrUpdateMenu-form');
    if (addOrUpdateMenuForm) {
        addOrUpdateMenuForm.addEventListener('submit', (event) => {
            event.preventDefault();
            const formData = new FormData(addOrUpdateMenuForm);
            const menu = {
                id: formData.get('id'),
                name: formData.get('name'),
                description: formData.get('description'),
                price: parseFloat(formData.get('price')), // Convertir el precio a número de punto flotante
                category_id: formData.get('category_id'),
                image: formData.get('menuImageInput'),
            };
            console.log('menu', menu);
            addOrUpdateMenu(menu);
        });
    }
    document.getElementById('menuImageInput').addEventListener('change', function(event) {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = function(e) {
                const imgElement = document.getElementById('menuImageThumbnail');
                imgElement.src = e.target.result;
                imgElement.style.display = 'block';
            };
            reader.readAsDataURL(file);
        }
    });

=======
>>>>>>> cfdd15b (IMPLEMENTAR: agregar eventos de formulario de login y registro en customCode.js)
};

//*******************************************************************************************
// Codigo general que se ejecutará en todas las vistas de la aplicación
// ***************************************************************************************

//login, esta función se encarga de hacer el login del usuario
async function login(email, password) {
    routerInstance.showLoading();
    try {
        const isAuthenticated = await authService.login(email, password);
        if (isAuthenticated) {
            window.history.pushState({}, '', '/');
            routerInstance.router();
        } else {
            alert('Invalid credentials');
        }
    } catch (error) {
        console.error('Login error:', error);
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
<<<<<<< HEAD
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
=======
        if (register) {
            window.history.pushState({}, '', '/login');
            routerInstance.router();
        } else {
            alert('error al registrar');
>>>>>>> cfdd15b (IMPLEMENTAR: agregar eventos de formulario de login y registro en customCode.js)
        }
    } catch (error) {
        console.error('Register error:', error);
    }
    routerInstance.hideLoading();
}
<<<<<<< HEAD

// añadir o actualizar un menu usando menuService
async function addOrUpdateMenu(menu) {
    routerInstance.showLoading();

    //si esta definido el id del menu, entonces es una actualización
    if (menu.id) {
        await updateMenu(menu);
    } else {
        try {
            const response = await menuService.createMenuItem(menu);
            if (response.success) {
                window.history.pushState({}, '', '/');
                routerInstance.router();
            } else {
                alert('Error: Could not add or update menu');
            }
        } catch (error) {
            console.error('Add or update menu error:', error);
        }
    }

   
    routerInstance.hideLoading();
}

=======
>>>>>>> cfdd15b (IMPLEMENTAR: agregar eventos de formulario de login y registro en customCode.js)
