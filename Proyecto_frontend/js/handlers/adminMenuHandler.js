import menuService from  '../menuService.js';
import { routerInstance } from '../router.js';

class AdminMenuHandler {
    constructor() {
        this.addOrUpdateMenuForm = document.getElementById('addOrUpdateMenu-form');
        this.menuImageInput = document.getElementById('menuImageInput');
        this.categorySelect = document.getElementById('menu_category_id');
        this.menuTable = document.getElementById('menu-table');
    }

    async init() {
        this.setupAddOrUpdateMenuForm();
        this.setupMenuImageInput();
        this.setupButtonShow();
        this.setupButtonCloseModal();
        await this.populateCategorySelect();
        await this.populateMenuTable();
    }

    setupAddOrUpdateMenuForm() {
        if (this.addOrUpdateMenuForm) {
            this.addOrUpdateMenuForm.addEventListener('submit', (event) => {
                event.preventDefault();
                const formData = new FormData(this.addOrUpdateMenuForm);
                const menu = {
                    id: formData.get('id'),
                    name: formData.get('name'),
                    description: formData.get('description'),
                    price: parseFloat(formData.get('price')), // Convertir el precio a número de punto flotante
                    category_id: formData.get('category_id'),
                };
                console.log('menu', menu);
                addOrUpdateMenu(menu);
            });
        }
    }

    setupMenuImageInput() {
        if (this.menuImageInput) {
            this.menuImageInput.addEventListener('change', function(event) {
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
    }

    async populateCategorySelect() {
        if (this.categorySelect) {
            // Limpiamos el listbox
            this.categorySelect.innerHTML = '';
            // Agregamos la categoría 0 por defecto
            const defaultOption = document.createElement('option');
            defaultOption.value = 0;
            defaultOption.innerText = 'Select a category';
            this.categorySelect.appendChild(defaultOption);

            try {
                const response = await menuService.getCategories();
                const categories = response.data;
                if (Array.isArray(categories)) {
                    categories.forEach((category) => {
                        const option = document.createElement('option');
                        option.value = category.id;
                        option.innerText = category.name;
                        this.categorySelect.appendChild(option);
                    });
                } else {
                    console.error('Expected an array but got:', categories);
                }
            } catch (error) {
                console.error('Error fetching categories:', error);
            }
        }
    }

    async populateMenuTable() {
        if (this.menuTable) {
            try {
                const categoriesResponse = await menuService.getCategories();
                const categories = categoriesResponse.data;

                // Crear un mapa de categorías para un acceso rápido
                const categoryMap = {};
                if (Array.isArray(categories)) {
                    categories.forEach((category) => {
                        categoryMap[category.id] = category.name;
                    });
                }

                const response = await menuService.getAllMenuItems();
                const menus = response.data;
                if (Array.isArray(menus)) {
                    for (const menu of menus) {
                        const tr = document.createElement('tr');
                        tr.setAttribute('data-id', menu.id);

                        // Get the image content from the server
                        let imageUrl = '';
                        if (menu.photo) {
                            imageUrl = await menuService.getImagefromServer(menu.photo);
                        }

                        tr.innerHTML = `
                            <td><img src="${imageUrl}" alt="Photo" width="100"></td>
                            <td>${menu.name}</td>
                            <td>${menu.description}</td>
                            <td>${menu.price}</td>
                            <td>${categoryMap[menu.category_id] || 'Unknown'}</td>
                            <td>
                                <button class="btn btn-primary edit-menu" data-id="${menu.id}">Edit</button>
                                <button class="btn btn-danger delete-menu" data-id="${menu.id}">Delete</button>
                            </td>
                        `;
                        this.menuTable.appendChild(tr);
                    }

                    this.setupDeleteButtons();
                    this.setupEditButtons();
                } else {
                    console.error('Expected an array but got:', menus);
                }
            } catch (error) {
                console.error('Error fetching menus:', error);
            }
        }
    }

    setupDeleteButtons() {
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
    }

    setupButtonShow() {
        //agregamos un evento al boton de mostrar formulario
        const showFormButton = document.getElementById('admin-menu-show-add');
        if (showFormButton) {
            showFormButton.addEventListener('click', async (event) => {
                const menuAddEditAdmin = document.getElementById('menu-add-edit-admin');
                if (menuAddEditAdmin) {
                    menuAddEditAdmin.style.display = 'block';
                    menuAddEditAdmin.scrollIntoView({ behavior: 'smooth' });

                    //borramos el contenido del formulario
                    document.getElementById('id').value ="";
                    document.getElementById('name').value = '';
                    document.getElementById('description').value = '';
                    document.getElementById('price').value ='';
                    document.getElementById('menu_category_id').value = 0;
                    document.getElementById('menuImageThumbnail').src = '';
                    document.getElementById('menuImageThumbnail').style.display = menu.photo ? 'block' : 'none';
                    document.querySelector('#addOrUpdateMenu-form button[type="submit"]').innerText = 'Agregar Plato';

                }
            });
        }
    }

    setupButtonCloseModal() {
        //agregamos un evento al boton de cerrar formulario
        const closeFormButton = document.getElementById('closeAdminMenuForm');
        if (closeFormButton) {
            closeFormButton.addEventListener('click', async (event) => {
                const menuAddEditAdmin = document.getElementById('menu-add-edit-admin');
                if (menuAddEditAdmin) {
                    menuAddEditAdmin.style.display = 'none';
                }
            });
        }
    }

    

            


    setupEditButtons() {
        const editButtons = document.getElementsByClassName('edit-menu');
        for (let i = 0; i < editButtons.length; i++) {
            editButtons[i].addEventListener('click', async (event) => {
                const id = event.target.getAttribute('data-id');
                const menu = await menuService.getMenuItemById(id);
                if (menu) {
                    //mostramos el formulario de añadir o actualizar menu menu-add-edit-admin
                    const menuAddEditAdmin = document.getElementById('menu-add-edit-admin');
                    if (menuAddEditAdmin) {
                        menuAddEditAdmin.style.display = 'block';
                        menuAddEditAdmin.scrollIntoView({ behavior: 'smooth' });
                    }


                    document.getElementById('addOrUpdateMenu-form').style.display = 'block';
                    document.getElementById('id').value = menu.id;
                    document.getElementById('name').value = menu.name;
                    document.getElementById('description').value = menu.description;
                    document.getElementById('price').value = menu.price;
                    document.getElementById('menu_category_id').value = menu.category_id || 0;
                    document.getElementById('menuImageThumbnail').src = await menuService.getImagefromServer(menu.photo);
                    document.getElementById('menuImageThumbnail').style.display = menu.photo ? 'block' : 'none';
                    document.querySelector('#addOrUpdateMenu-form button[type="submit"]').innerText = 'Actualizar Plato';
                }
            });
        }
    }


    

}

// añadir o actualizar un menu usando menuService
async function addOrUpdateMenu(menu) {
    routerInstance.showLoading();

    //si esta definido el id del menu, entonces es una actualización
    if (menu.id) {
        try {
            const lastImage = document.getElementById('menuImageThumbnail').src;
            const response = await menuService.updateMenuItem(menu.id, menu,document.getElementById('menuImageInput').files[0],lastImage);
            if (response) {
                alert('Menu updated successfully');
                routerInstance.router();
            } else {
                alert('Error: Could not add or update menu');
            }
        } catch (error) {
            alert('Error: Could not add or update menu');
            console.error('Add menu error:', error);
        }
        
    } else {
        try {
            const response = await menuService.createMenuItem(menu, document.getElementById('menuImageInput').files[0]);
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

export default AdminMenuHandler;