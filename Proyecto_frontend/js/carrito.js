// Clase Carrito para manejar la lógica del carrito de compras
class Carrito {
    constructor() {
        this.platos = [];
    }

    añadirPlato(itemMenuDTO) {
        const plato = this.platos.find(p => p.id === itemMenuDTO.id);
        if (plato) {
            plato.cantidad++;
        } else {
            this.platos.push({ ...itemMenuDTO, cantidad: 1 });
        }
        this.actualizarCarrito();
    }

    quitarPlato(id) {
        this.platos = this.platos.filter(p => p.id !== id);
        this.actualizarCarrito();
    }

    borrarTodo() {
        this.platos = [];
        this.actualizarCarrito();
    }

    actualizarCantidad(id, cantidad) {
        const plato = this.platos.find(p => p.id === id);
        if (plato) {
            plato.cantidad = cantidad;
            if (plato.cantidad <= 0) {
                this.quitarPlato(id);
            } else {
                this.actualizarCarrito();
            }
        }
    }

    confirmarCompra() {
        if (this.platos.length === 0) {
            console.log("El carrito está vacío.");
        } else {
            console.log("Compra confirmada:");
            this.platos.forEach(plato => {
                console.log(`${plato.name} - $${plato.price} x ${plato.cantidad}`);
            });
            this.borrarTodo();
        }
    }

    actualizarCarrito() {
        const carritoLista = document.querySelector('.carrito-lista');
        const totalSpan = document.querySelector('.total');
        const ordersTable = document.querySelector('.orders-table tbody');
        
        carritoLista.innerHTML = '';
        ordersTable.innerHTML = '';
        
        let total = 0;
        this.platos.forEach(plato => {
            // Actualizar la lista del carrito
            const li = document.createElement('li');
            li.textContent = `${plato.name} - $${plato.price} x ${plato.cantidad}`;
            carritoLista.appendChild(li);
            
            // Actualizar la tabla de pedidos
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${plato.name}</td>
                <td>${plato.cantidad}</td>
                <td>$${(plato.price * plato.cantidad).toFixed(2)}</td>
                <td>${new Date().toLocaleString()}</td>
                <td>En proceso</td>
                <td><button class="quitar-plato" data-id="${plato.id}">Quitar</button></td>
            `;
            ordersTable.appendChild(tr);

            total += plato.price * plato.cantidad;
        });
        totalSpan.textContent = total.toFixed(2);
    }
}

// document.addEventListener('DOMContentLoaded', () => {
//     const menuTable = document.querySelector('#menu-table tbody');
//     if (menuTable === null) {
//         console.error("El elemento menuTable no se encontró en el DOM.");
//         return;
//     }

//     const miCarrito = new Carrito();

//     // Agregar platos al menú
//     const menuPlatos = [
//         new ItemMenuDTO(1, "Ensalada", "Una ensalada fresca", 10, "url/to/ensalada.jpg", 1),
//         new ItemMenuDTO(2, "Pizza", "Deliciosa pizza italiana", 15, "url/to/pizza.jpg", 2),
//         new ItemMenuDTO(3, "Hamburguesa", "Jugosa hamburguesa con queso", 12, "url/to/hamburguesa.jpg", 2),
//         new ItemMenuDTO(4, "Pasta", "Pasta casera con salsa", 13, "url/to/pasta.jpg", 2),
//         new ItemMenuDTO(5, "Sushi", "Sushi variado y fresco", 20, "url/to/sushi.jpg", 2)
//     ];

//     menuPlatos.forEach(plato => {
//         const tr = document.createElement('tr');
//         tr.innerHTML = `
//             <td><img src="${plato.image}" alt="${plato.name}" width="50"></td>
//             <td>${plato.name}</td>
//             <td>${plato.description}</td>
//             <td>$${plato.price.toFixed(2)}</td>
//             <td>${plato.categoryId}</td>
//             <td><button class="add-to-cart" data-id="${plato.id}" data-name="${plato.name}" data-price="${plato.price}">Agregar al Carrito</button></td>
//         `;
//         menuTable.appendChild(tr);
//     });

//     // Event listeners
//     document.querySelectorAll('.add-to-cart').forEach(button => {
//         button.addEventListener('click', (evento) => {
//             const producto = evento.target.closest('button');
//             const id = producto.dataset.id;
//             const name = producto.dataset.name;
//             const price = parseFloat(producto.dataset.price);
//             const item = new ItemMenuDTO(id, name, '', price, '', 1);
//             miCarrito.añadirPlato(item);
//         });
//     });

//     document.querySelector('.borrar-todo').addEventListener('click', () => {
//         miCarrito.borrarTodo();
//     });

//     document.querySelector('.confirmar-compra').addEventListener('click', () => {
//         miCarrito.confirmarCompra();
//     });

//     document.querySelector('.orders-table tbody').addEventListener('click', (evento) => {
//         if (evento.target.classList.contains('quitar-plato')) {
//             const id = evento.target.dataset.id;
//             miCarrito.quitarPlato(id);
//         }
//     });
// });

