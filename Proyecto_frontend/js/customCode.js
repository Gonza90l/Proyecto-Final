// CustomCode.js
// Aqui se declara todo el código accesorio que se necesita para que la aplicación funcione correctamente. Este archivo no se debe modificar.
import authService from './authService.js';
import { routerInstance } from './router.js';
import menuService from './menuService.js';

routerInstance.onViewLoaded = () => {
    console.log('onViewLoaded function executed');
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
    const menuImageInput = document.getElementById('menuImageInput');
    if (menuImageInput) {
        menuImageInput.addEventListener('change', function(event) {
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
    }

    //agregamos las cateogrias al listbox de categorias
    const categorySelect = document.getElementById('menu_category_id');
    if (categorySelect) {
        //limpiamos el listbox
        categorySelect.innerHTML = '';
        //agregamos la cartegoi 0 por defecto
        const defaultOption = document.createElement('option');
        defaultOption.value = 0;
        defaultOption.innerText = 'Select a category';
        categorySelect.appendChild(defaultOption);

        menuService.getCategories().then((response) => {
            const categories = response.data;
            if (Array.isArray(categories)) {
                categories.forEach((category) => {
                    const option = document.createElement('option');
                    option.value = category.id;
                    option.innerText = category.name;
                    categorySelect.appendChild(option);
                });
            } else {
                console.error('Expected an array but got:', categories);
            }
        }).catch((error) => {
            console.error('Error fetching categories:', error);
        });
    }

    // listar los menus en la menu-table
    const menuTable = document.getElementById('menu-table');
    if (menuTable) {
        menuService.getAllMenuItems().then((response) => {
            const menus = response.data;
            if (Array.isArray(menus)) {
                menus.forEach((menu) => {
                    const tr = document.createElement('tr');
                    tr.setAttribute('data-id', menu.id);
                    tr.innerHTML = `
                    <td>${menu.name}</td>
                    <td>${menu.description}</td>
                    <td>${menu.price}</td>
                    <td>categoria</td>
                    <td>
                        <button class="btn btn-primary edit-menu" data-id="${menu.id}">Edit</button>
                        <button class="btn btn-danger delete-menu" data-id="${menu.id}">Delete</button>
                    </td>
                    `;
                    menuTable.appendChild(tr);
                });

                // agregar evento al boton de delete
                const deleteButtons = document.getElementsByClassName('delete-menu');
                for (let i = 0; i < deleteButtons.length; i++) {
                    deleteButtons[i].addEventListener('click', async (event) => {
                        const id = event.target.getAttribute('data-id');
                        if (confirm('Are you sure you want to delete this menu?')) {
                            await menuService.deleteMenuItem(id);
                            routerInstance.router();
                        }
                    });
                }

                // agregar evento al boton de edit
                const editButtons = document.getElementsByClassName('edit-menu');
                for (let i = 0; i < editButtons.length; i++) {
                    editButtons[i].addEventListener('click', async (event) => {
                        const id = event.target.getAttribute('data-id');
                        const menu = await menuService.getMenuItemById(id);
                        if (menu) {
                            document.getElementById('id').value = menu.id;
                            document.getElementById('name').value = menu.name;
                            document.getElementById('description').value = menu.description;
                            document.getElementById('price').value = menu.price;
                            document.getElementById('menu_category_id').value = menu.category_id;
                            document.getElementById('menuImageThumbnail').src = menu.image_url;
                            document.getElementById('menuImageThumbnail').style.display = 'block';
                            document.querySelector('#addOrUpdateMenu-form button[type="submit"]').innerText = 'Actualizar Plato';
                        }
                    });
                }
            } else {
                console.error('Expected an array but got:', menus);
            }
        }).catch((error) => {
            console.error('Error fetching menus:', error);
        });
    }

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

// añadir o actualizar un menu usando menuService
async function addOrUpdateMenu(menu) {
    routerInstance.showLoading();

    //si esta definido el id del menu, entonces es una actualización
    if (menu.id) {
        await updateMenu(menu);
    } else {
        try {
            const response = await menuService.createMenuItem(menu);
            if (response) {
                alert('Menu added successfully');
                routerInstance.router();
            } else {
                alert('Error: Could not add or update menu');
            }
        }catch (error) {
            alert('Error: Could not add or update menu \n' + JSON.stringify(error.data.errors));
            console.error('Add menu error:', error);
        }

    }

    routerInstance.hideLoading();
}

