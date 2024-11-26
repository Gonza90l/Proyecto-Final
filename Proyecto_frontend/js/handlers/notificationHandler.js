import authService from '../authService.js';
import notificationsService from '../notificationService.js';
import { routerInstance } from '../router.js';

var intervalId = null; // Almacena el ID del intervalo

class NotificationHandler {
    constructor() {
        this.previousNotificationCount = 0; // Almacena el contador de notificaciones anterior
        this.eventsAdded = false; // Variable de estado para rastrear si los eventos ya han sido agregados
    }

    async init() {
        if (!authService.isAuthenticated()) {
            return;
        }

        this.ensureModalExists();
        await this.renderNotifications();

        if (!this.eventsAdded) {
            // Eliminar eventos existentes y añadir nuevos eventos
            this.addEventListener('notificaction-icon', 'click', openModal.bind(this));
            this.addEventListener('close-modal', 'click', closeModal.bind(this));
            this.addEventListener('mark-all-read', 'click', markAllAsRead.bind(this));
            this.addEventListener(window, 'click', handleWindowClick.bind(this));

            // Marcar que los eventos han sido agregados
            this.eventsAdded = true;
        }

        // Verificar nuevas notificaciones cada minuto
        if (!intervalId) {
            intervalId = setInterval(async () => {
                await this.renderNotifications('interval');
            }, 15000); // 15 segundos
        }
    }

    addEventListener(elementId, event, handler) {
        const element = elementId === window ? window : document.getElementById(elementId);
        if (element) {
            const eventKey = `${elementId}-${event}`;
            if (!element[eventKey]) {
                element.addEventListener(event, handler);
                element[eventKey] = true;
            }
        }
    }

    ensureModalExists() {
        if (!document.getElementById('notification-modal')) {
            const modalHtml = `
                <div id="notification-modal" class="modal">
                    <div class="modal-content">
                        <span class="close-button" id="close-modal">&times;</span>
                        <h2>Notificaciones</h2>
                        <button id="mark-all-read">Marcar todo como leído</button>
                        <ul id="notification-list"></ul>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
        }
    }

    async renderNotifications(flag = null) {
        const notifications = await this.getAllNotifications();
        
        let notifications_counter = 0;
        if (notifications.data != undefined && notifications.data.length > 0) {
            notifications_counter = notifications.data.filter(notification => notification.read_at === null).length;
        }

        // Comparar el contador actual con el anterior
        if (flag === 'interval' && notifications_counter > this.previousNotificationCount) {
            routerInstance.showNotification(`Tienes ${notifications_counter} notificaciones nuevas`, 'info');
        }

        // Actualizar el contador de notificaciones anterior
        this.previousNotificationCount = notifications_counter;

        const notificationList = document.getElementById('notification-count');
        if (notificationList) {
            if (notifications_counter === 0) {
                notificationList.style.display = 'none';
            } else {
                notificationList.style.display = 'block';
            }
            notificationList.innerHTML = notifications_counter;
        }

        const notificationIcon = document.getElementById('notificaction-icon');
        if (notificationIcon) {
            if (notifications_counter > 0) {
                notificationIcon.classList.add('notification-active');
            } else {
                notificationIcon.classList.remove('notification-active');
            }
        }

        this.populateNotificationList(notifications.data);
    }

    async getAllNotifications() {
        if (!authService.isAuthenticated()) {
            return [];
        }
        try {
            const notifications = await notificationsService.getAllNotifications();
            return notifications;
        } catch (error) {
            console.error('Error fetching notifications:', error);
            return [];
        }
    }

    populateNotificationList(notifications) {
        const notificationList = document.getElementById('notification-list');
        //filtramos las notificaciones no leídas
        notifications = notifications.filter(notification => notification.read_at === null);
        if (notificationList) {
            notificationList.innerHTML = '';
            notifications.forEach(notification => {
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <div>
                        <p><strong>${notification.subject}</strong></p>
                        <p>${notification.body}</p>
                        <p><small>${new Date(notification.created_at).toLocaleString()}</small></p>
                    </div>
                `;
                listItem.addEventListener('click', () => {
                    this.markAsRead(notification.id);
                });
                notificationList.appendChild(listItem);
            });
        }
        //si no hay notificaciones no leídas ocultamos el botón de marcar todas como leídas
        const markAllReadButton = document.getElementById('mark-all-read');
        if (markAllReadButton) {
            if (notifications.length === 0) {
                markAllReadButton.style.display = 'none';
                //agregamos un mensaje de que no hay notificaciones
                const listItem = document.createElement('li');
                listItem.innerHTML = `
                    <div>
                        <p><strong>No hay notificaciones</strong></p>
                    </div>
                `;
                notificationList.appendChild(listItem);

            } else {
                markAllReadButton.style.display = 'block';
                
            }
        }
    }

    async markAsRead(notificationId) {
        try {
            await notificationsService.markNotificationAsRead(notificationId);
            await this.renderNotifications();
        } catch (error) {
            console.error('Error marking notification as read:', error);
        }
    }

    
}


async function markAllAsRead() {
    const notifications = await this.getAllNotifications();
    const unreadNotifications = notifications.data.filter(notification => notification.read_at === null);
    unreadNotifications.forEach(async notification => {
        await this.markAsRead(notification.id);
    });
    //ocultamos el modal
    closeModal();
}

// Event handler functions
function openModal() {
    const modal = document.getElementById('notification-modal');
    if (modal) {
        modal.style.display = 'block';
    }
}

function closeModal() {
    const modal = document.getElementById('notification-modal');
    if (modal) {
        modal.style.display = 'none';
    }
}

function handleWindowClick(event) {
    const modal = document.getElementById('notification-modal');
    if (event.target === modal) {
        closeModal();
    }
}

export default NotificationHandler;