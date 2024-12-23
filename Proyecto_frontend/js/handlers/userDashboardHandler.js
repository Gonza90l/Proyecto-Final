import ordersService from "../orderService.js";
import reviewService from "../reviewService.js";
import { routerInstance } from "../router.js";

class UserDashboardHandler {

    constructor() {
        
    }

    init() {
        this.renderUserDashboard();
        this.addEvents();
    }

    async addEvents(){
        //añadimos el evento de cerrar al modal
        if(document.getElementById('close-add-reviews-modal')){
            document.getElementById('close-add-reviews-modal').addEventListener('click', () => {
                document.getElementById('review-modal').style.display = 'none';
            });
        }

        const form = document.getElementById('review-form');
        if (form) {
            
            // Escuchar el evento de envío del formulario
            // Obtener el ID del pedido del formulario
            
            form.addEventListener('submit', async (event) => {
                event.preventDefault(); // Prevenir el envío del formulario por defecto
                const orderId = form['order-id'].value;
                const order = await ordersService.getOrderById(orderId);
                
                // Recoger todos los datos del formulario
                const formData = new FormData(form);
                const data = [];
                const orderItems = order.order_items;

                orderItems.forEach((orderItem, index) => {
                    const reviewData = {
                        order_id: parseInt(orderId),
                        id: parseInt(formData.get(`dish-id-${index}`)),
                        rating: parseInt(formData.get(`rating-${index}`)),
                        review: formData.get(`review-${index}`)
                    };
                    data.push(reviewData);
                });

                try {
                    // Llamar al servicio de reseñas
                    await reviewService.createReview(data); // Asumiendo que `addReviews` acepta un array de reseñas
                    routerInstance.showNotification('Reseñas enviadas con éxito','info');
                    routerInstance.navigate('/dashboard');
                } catch (error) {
                    console.error('Error al enviar las reseñas:', error);
                    routerInstance.showNotification('Error al enviar las reseñas', 'danger');
                }
            });
        }
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
        async function createOrderRow(order, includeActions = true) {
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
                const hasComments = await reviewService.getReviewByOrderId(order.id);
                if (!hasComments) {
                    let btnComentarios = document.createElement("button");
                    btnComentarios.classList.add("add-review");
                    btnComentarios.title = "Agregar Comentarios y Reseñas";
                    btnComentarios.innerHTML = '<i class="fas fa-comment"></i>';
                    btnComentarios.addEventListener('click', () => {
                        addReview(order.id);
                    });
                    tdEstado.appendChild(btnComentarios);
                }
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
                if (order.status === 'CREATED' || order.status === 'PAID') {
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
            }
        
            return tr;
        }
    
        // iteramos los pedidos activos
        for (const order of ordersActive) {
            let tr = await createOrderRow(order, true);
            tbodyActive.appendChild(tr);
        }
    
        // iteramos los pedidos inactivos
        for (const order of ordersInactive) {
            let tr = await createOrderRow(order, false);
            tbodyInactive.appendChild(tr);
        }
    }
}

// Métodos para actualizar y cancelar pedidos
function updateOrder(orderId) {
    // Lógica para actualizar el pedido
}

async function cancelOrder(orderId) {
    // Preguntamos al usuario si está seguro
    if (!confirm('¿Está seguro de que desea cancelar el pedido?')) {
        return;
    }
    //obtenemos el pedido
    let orderData = await ordersService.getOrderById(orderId);
    if (!orderData) {
        routerinstance.showNotification('No se pudo obtener el pedido', 'danger');
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

async function addReview(orderId) {
    // Obtener el modal y el formulario
    const modal = document.getElementById('review-modal');
    const form = document.getElementById('review-form');
    
    // Llenar el campo de ID del Pedido
    form['order-id'].value = orderId;
    
    // Obtener el contenedor de secciones de reseñas
    const reviewSections = document.getElementById('review-sections');
    
    // Limpiar las secciones anteriores
    reviewSections.innerHTML = '';
    
    // Obtener los platos del pedido
    const order = await ordersService.getOrderById(orderId);
    order.order_items.forEach((orderItem, index) => {
        const section = document.createElement('div');
        section.classList.add('review-section');

        const dishLabel = document.createElement('label');
        dishLabel.textContent = `Nombre del Plato: ${orderItem.item.name}`;
        section.appendChild(dishLabel);

        const dishInput = document.createElement('input');
        dishInput.type = 'hidden';
        dishInput.name = `dish-id-${index}`;
        dishInput.value = orderItem.item.id;
        section.appendChild(dishInput);

        const ratingLabel = document.createElement('label');
        ratingLabel.textContent = 'Calificación:';
        section.appendChild(ratingLabel);

        const ratingSelect = document.createElement('select');
        ratingSelect.name = `rating-${index}`;
        ratingSelect.innerHTML = `
            <option value="1">1 - Muy Malo</option>
            <option value="2">2 - Malo</option>
            <option value="3">3 - Regular</option>
            <option value="4">4 - Bueno</option>
            <option selected value="5">5 - Muy Bueno</option>
        `;
        section.appendChild(ratingSelect);

        const reviewLabel = document.createElement('label');
        reviewLabel.textContent = 'Reseña:';
        section.appendChild(reviewLabel);

        const reviewTextarea = document.createElement('textarea');
        reviewTextarea.name = `review-${index}`;
        section.appendChild(reviewTextarea);

        reviewSections.appendChild(section);
    });
    
    // Mostrar el modal
    modal.style.display = 'block';
}

// Implementa la función getOrderById para obtener el pedido por ID
async function getOrderById(orderId) {
    return await ordersService.getOrderById(orderId);
}

export default UserDashboardHandler;