import { routerInstance } from '../router.js';
import ordersService from "../orderService.js";

class AdminOrdersHandler {

    constructor() {
        
    }

    async init() {
        console.log('AdminOrdersHandler initialized');
        this.renderOrders();
    }

    async renderOrders() {

        // renderizamos la tabla de pedidos
        // ubicamos el tbody user-orders-active y user-orders-inactive
        let tbodyActive = document.getElementById("admin-orders-active");
        if (!tbodyActive) {
            return;
        }
    
        // borramos el contenido de los tbodys
        tbodyActive.innerHTML = "";
    
        // obtenemos los pedidos del usuario
        let orders = await ordersService.getAllOrders();
    
        // ordenamos los pedidos por fecha de creación
        orders.sort((a, b) => {
            return new Date(b.created_at) - new Date(a.created_at);
        });
    
        // creamos una lista con los 'CREATED','PAID','IN PROGRESS','SEND' y otra con los 'DELIVERED','CANCELED'
        let ordersActive = orders.filter(order => [ 'PAID', 'IN PROGRESS', 'SEND'].includes(order.status));

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
                if (order.status === 'CREATED' || order.status === 'PAID' || order.status === 'IN PROGRESS' || order.status === 'SEND') {
                    let btnActualizar = document.createElement("button");
                    btnActualizar.classList.add("update-order");
                    btnActualizar.title = "Actualizar Pedido";
                    btnActualizar.innerHTML = '<i class="fas fa-edit"></i>';
                    btnActualizar.addEventListener('click', () => {
                        showUpdateModal(order.id);
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

    }
}

async function showUpdateModal(orderId) {
    // Obtener el modal y el formulario
    const modal = document.getElementById('update-modal');
    const form = document.getElementById('update-form');
    
    if(!modal || !form) {
        console.error('No se encontró el modal o el formulario');
        return;
    }

    // Definir la función de envío del formulario
    const handleSubmit = async (event) => {
        event.preventDefault(); // Prevenir el envío del formulario por defecto
        
        // Recoger los datos del formulario
        const formData = new FormData(form);
        const newStatus = formData.get('status');
        
        try {
            // Obtener el pedido
            let orderData = await ordersService.getOrderById(orderId);
            if (!orderData) {
                routerInstance.showNotification('No se pudo obtener el pedido', 'danger');
                return;
            }
            
            // Actualizar el estado del pedido
            orderData.status = newStatus;
            
            // Llamar al servicio de pedidos para actualizar el pedido
            await ordersService.updateOrder(orderId, orderData);
            
            // Actualizar la tabla de pedidos
            routerInstance.navigate('/admin-orders');
            
            // Ocultar el modal
            modal.style.display = 'none';
            
            routerInstance.showNotification('Pedido actualizado con éxito', 'info');
        } catch (error) {
            console.error('Error al actualizar el pedido:', error);
            routerInstance.showNotification('Error al actualizar el pedido', 'danger');
        }
    };

    // Eliminar cualquier evento anterior
    form.removeEventListener('submit', handleSubmit);

    // Llenar el campo de ID del Pedido
    form['order-id'].value = orderId;
    
    // Mostrar el modal
    modal.style.display = 'block';
    
    // Escuchar el evento de envío del formulario
    form.addEventListener('submit', handleSubmit);
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
        routerInstance.showNotification('No se pudo obtener el pedido', 'danger');
        return;
    }
    //cambiamos el estado del pedido a CANCELED
    orderData.status = 'CANCELED';
    //llamamos al orderService para cancelar el pedido
    ordersService.updateOrder(orderId,orderData).then(() => {
        // actualizamos la tabla de pedidos
        routerInstance.showNotification('Pedido cancelado con éxito', 'info');
        routerInstance.navigate('/admin-orders');
    });
}

export default AdminOrdersHandler;