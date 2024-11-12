import ordersService from "../orderService.js";


class UserDashboardHandler {

    constructor() {
        
    }

    init() {
        this.renderUserDashboard();
    }

    async renderUserDashboard() {
        // renderizamos la tabla de pedidos
        // ubicamos el tbody user-orders-active y user-orders-inactive
        let tbodyActive = document.getElementById("user-orders-active");
        let tbodyInactive = document.getElementById("user-orders-inactive");
        if (!tbodyActive || !tbodyInactive) {
            return;
        }
    
        // borramos el contenido de los tbodys
        tbodyActive.innerHTML = "";
        tbodyInactive.innerHTML = "";
    
        // obtenemos los pedidos del usuario
        let orders = await ordersService.getAllOrders();
    
        // ordenamos los pedidos por fecha de creación
        orders.sort((a, b) => {
            return new Date(b.created_at) - new Date(a.created_at);
        });
    
        // creamos una lista con los 'CREATED','PAID','IN PROGRESS','SEND' y otra con los 'DELIVERED','CANCELED'
        let ordersActive = orders.filter(order => ['CREATED', 'PAID', 'IN PROGRESS', 'SEND'].includes(order.status));
        let ordersInactive = orders.filter(order => ['DELIVERED', 'CANCELED'].includes(order.status));
    
        // Mapeo de estados en inglés a castellano
        const statusMap = {
            'CREATED': 'Creado',
            'PAID': 'Pagado',
            'IN PROGRESS': 'En Progreso',
            'SEND': 'Enviado',
            'DELIVERED': 'Entregado',
            'CANCELED': 'Cancelado'
        };
    
        // función para crear una fila de pedido
        function createOrderRow(order, includeActions = true) {
            // creamos una nueva fila
            let tr = document.createElement("tr");
        
            // creamos las celdas de la fila
            let tdPedido = document.createElement("td");
            tdPedido.textContent = `Pedido #${order.id}`;
        
            let tdFechaHora = document.createElement("td");
            tdFechaHora.textContent = new Date(order.created_at).toLocaleString();
        
            let tdPlatos = document.createElement("td");
            let ulPlatos = document.createElement("ul");
            ulPlatos.classList.add("order-items");
            order.order_items.forEach(orderItem => {
                let li = document.createElement("li");
                li.textContent = `${orderItem.item.name}, Cantidad: ${orderItem.quantity}, Precio: $${orderItem.item.price}`;
                ulPlatos.appendChild(li);
            });
            tdPlatos.appendChild(ulPlatos);
        
            let tdPrecioTotal = document.createElement("td");
            tdPrecioTotal.textContent = `$${order.total}`;
        
            let tdEstado = document.createElement("td");
            let spanEstado = document.createElement("span");
            spanEstado.classList.add("status", order.status.toLowerCase().replace(/\s+/g, '_'));
            spanEstado.textContent = statusMap[order.status] || order.status; // Mapeamos el estado al castellano
            tdEstado.appendChild(spanEstado);
        
            // Añadir botón de comentarios y reseñas si el estado es "DELIVERED"
            if (order.status === 'DELIVERED') {
                let btnComentarios = document.createElement("button");
                btnComentarios.classList.add("add-review");
                btnComentarios.title = "Agregar Comentarios y Reseñas";
                btnComentarios.innerHTML = '<i class="fas fa-comment"></i>';
                btnComentarios.addEventListener('click', () => {
                    addReview(order.id);
                });
                tdEstado.appendChild(btnComentarios);
            }
        
            // añadimos las celdas a la fila
            tr.appendChild(tdPedido);
            tr.appendChild(tdFechaHora);
            tr.appendChild(tdPlatos);
            tr.appendChild(tdPrecioTotal);
            tr.appendChild(tdEstado);
        
            // Añadimos la columna de acciones solo si includeActions es true
            if (includeActions) {
                let tdAcciones = document.createElement("td");
                if (order.status === 'CREATED') {
                    let btnActualizar = document.createElement("button");
                    btnActualizar.classList.add("update-order");
                    btnActualizar.title = "Actualizar Pedido";
                    btnActualizar.innerHTML = '<i class="fas fa-edit"></i>';
                    btnActualizar.addEventListener('click', () => {
                        updateOrder(order.id);
                    });
                    tdAcciones.appendChild(btnActualizar);
                }
                let btnCancelar = document.createElement("button");
                btnCancelar.classList.add("cancel-order");
                btnCancelar.title = "Cancelar Pedido";
                btnCancelar.innerHTML = '<i class="fas fa-times"></i>';
                btnCancelar.addEventListener('click', () => {
                    cancelOrder(order.id);
                });
                tdAcciones.appendChild(btnCancelar);
                tr.appendChild(tdAcciones);
            }
        
            return tr;
        }
    
        // iteramos los pedidos activos
        ordersActive.forEach(order => {
            let tr = createOrderRow(order, true);
            tbodyActive.appendChild(tr);
        });
    
        // iteramos los pedidos inactivos
        ordersInactive.forEach(order => {
            let tr = createOrderRow(order, false);
            tbodyInactive.appendChild(tr);
        });
    }
}

// Métodos para actualizar y cancelar pedidos
function updateOrder(orderId) {
    // Lógica para actualizar el pedido
    console.log(`Actualizar pedido ${orderId}`);
}

async function cancelOrder(orderId) {
    // Preguntamos al usuario si está seguro
    if (!confirm('¿Está seguro de que desea cancelar el pedido?')) {
        return;
    }
    //obtenemos el pedido
    let orderData = await ordersService.getOrderById(orderId);
    console.log(orderData);
    if (!orderData) {
        routerinstance.showAlert('No se pudo obtener el pedido', 'danger');
        return;
    }
    //cambiamos el estado del pedido a CANCELED
    orderData.status = 'CANCELED';
    //llamamos al orderService para cancelar el pedido
    ordersService.updateOrder(orderId,orderData).then(() => {
        // actualizamos la tabla de pedidos
        let handler = new UserDashboardHandler();
        handler.renderUserDashboard();
    });
}

export default UserDashboardHandler;