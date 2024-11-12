import authService from '../authService.js';
import { routerInstance } from '../router.js';
import orderService from '../orderService.js';

class CheckOutHandler {

    constructor() {
        this.orderId = null;
        this.orderStatus = null;
        this.errormessage = null;
    }

    async init() {
        //si la ruta comienza con /checkout
        if (window.location.pathname.startsWith('/checkout')) {
            //si no viene el parametro ?order=
            if (!window.location.search.includes('?order=')) {
                //redirigir a la pagina principal
                routerInstance.showNotification('No se ha especificado un pedido para procesar', 'critical');
                routerInstance.navigate('/');
            }else{
                //averiguamos el estado del pedido en el orderService
                 this.orderId = window.location.search.split('=')[1];
                //si es numerico o lo podemos convertir a numero proseguimos
                if (!isNaN(this.orderId)) {
                    const order = await orderService.getOrderById(this.orderId); 
                    //colocamos en checkoutTotalAmount el total del pedido
                    document.getElementById('checkoutTotalAmount').textContent = order.total;
                }
            }
            this.errormessage = this.generateRandomCardMessage();
            this.configureEvents();
        }

    }

    async configureEvents() {
        // Agregamos un evento al formulario de checkout
        const checkoutForm = document.getElementById('checkoutForm');
        if (checkoutForm) {
            checkoutForm.addEventListener('submit', async (event) => {
                event.preventDefault();
    
                // Validaciones personalizadas
                const name = document.getElementById('name').value;
                const email = document.getElementById('email').value;
                const address = document.getElementById('address').value;
                const cardNumber = document.getElementById('card-number').value;
                const expiryDate = document.getElementById('expiry-date').value;
                const cvv = document.getElementById('cvv').value;
    
                const namePattern = /^[a-zA-Z\s]+$/;
                const cardNumberPattern = /^\d{16}$/;
                const expiryDatePattern = /^(0[1-9]|1[0-2])\/\d{2}$/;
                const cvvPattern = /^\d{3}$/;
    
                if (!namePattern.test(name)) {
                    routerInstance.showNotification('El nombre solo debe contener letras y espacios', 'critical');
                    return;
                }
    
                if (!checkoutForm.email.checkValidity()) {
                    routerInstance.showNotification('Correo electrónico no válido', 'critical');
                    return;
                }
    
                if (!address) {
                    routerInstance.showNotification('La dirección es requerida', 'critical');
                    return;
                }
    
                if (!cardNumberPattern.test(cardNumber)) {
                    routerInstance.showNotification('El número de tarjeta debe contener 16 dígitos', 'critical');
                    return;
                }
    
                if (!expiryDatePattern.test(expiryDate)) {
                    routerInstance.showNotification('La fecha de expiración debe estar en el formato MM/AA', 'critical');
                    return;
                }
    
                if (!cvvPattern.test(cvv)) {
                    routerInstance.showNotification('El CVV debe contener 3 dígitos', 'critical');
                    return;
                }


                //si el nombre es APRO 
                if (name !== 'APRO') {
                    //mostrar notificacion de error
                    routerInstance.showNotification(this.errormessage, 'critical');
                    return;
                }
                routerInstance.showNotification('Procesando pago...', 'info');
                //simulamos un push de la pasarela de pago

                //enviamos una solicitud IPN
                const response =  await orderService.sendIPNToServer({
                    orderId: this.orderId,
                    status: 'paid',
                    paymentMethod: 'credit_card',
                });

                if (!response) {
                    routerInstance.showNotification('La pasarela de pagos no pudo procesar la solicitud', 'critical');
                    return;
                }

                //Dado de que no se tiene un servicio de pago, se simula un tiempo de espera
                setTimeout(() =>  {                    
                    routerInstance.showNotification('Pago procesado exitosamente', 'info');
                    routerInstance.navigate('/');
                }, 2000);

                
            });
        }
    }

    //generar un mensaje de tarjeta aleatorio
    generateRandomCardMessage() {
        const messages = [
            'Pago rechazado, intente nuevamente',
            'Pago rechazado por falta de fondos',
            'Pago rechazado por error en la tarjeta',
            'El operador de la tarjeta ha rechazado el pago',
            'La pasarela de pago ha rechazado el pago',
            'Pago rechazado por error de comunicación',
            'Pago rechazado por error en el CVV',
            'Pago rechazado por error en la fecha de expiración',
            'Pago rechazado por error en el nombre del titular',
        ];
    
        // Generar un índice aleatorio
        const randomIndex = Math.floor(Math.random() * messages.length);
        return messages[randomIndex];
    }



}

export default  CheckOutHandler;