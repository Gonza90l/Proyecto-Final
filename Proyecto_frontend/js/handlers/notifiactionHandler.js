import authService from '../authService.js';
import notificationsService from '../notificationService.js';
import { routerInstance } from '../router.js';

class NotificationHandler {
    constructor() {}

    async init() {
        if (!authService.isAuthenticated()) {
            return;
        }

        this.ensureModalExists();
        await this.renderNotifications();

        // Event listener para abrir el modal
        const notificationIcon = document.getElementById('notificaction-icon');
        if (notificationIcon) {
            notificationIcon.addEventListener('click', () => {
                this.openModal();
            });
        }

        // Event listener para cerrar el modal
        const closeModal = document.getElementById('close-modal');
        if (closeModal) {
            closeModal.addEventListener('click', () => {
                this.closeModal();
            });
        }

        // Event listener para marcar todas las notificaciones como leídas
        const markAllReadButton = document.getElementById('mark-all-read');
        if (markAllReadButton) {
            markAllReadButton.addEventListener('click', () => {
                this.markAllAsRead();
            });
        }

        // Cerrar el modal si se hace clic fuera del contenido del modal
        window.addEventListener('click', (event) => {
            const modal = document.getElementById('notification-modal');
            if (event.target === modal) {
                this.closeModal();
            }
        });
    }

    ensureModalExists() {
        if (!document.getElementById('notification-modal')) {
            const modalHtml = `
                <div id="notification-modal" class="modal">
                    <div class="modal-content">
                        <span class="close" id="close-modal">&times;</span>
                        <h2>Notificaciones</h2>
                        <button id="mark-all-read">Marcar todo como leído</button>
                        <ul id="notification-list"></ul>
                    </div>
                </div>
            `;
            document.body.insertAdjacentHTML('beforeend', modalHtml);
        }
    }

    async renderNotifications() {
        const notifications = await this.getAllNotifications();
        
        let notifications_counter = 0;
        if (notifications.data != undefined && notifications.data.length > 0) {
            notifications_counter = notifications.data.filter(notification => notification.read_at === null).length;
        }

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
            console.log('Notifications:', notifications);
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

    async markAllAsRead() {
        const notifications = await this.getAllNotifications();
        const unreadNotifications = notifications.data.filter(notification => notification.read_at === null);
        unreadNotifications.forEach(async notification => {
            await this.markAsRead(notification.id);
        });
        //ocultamos el modal
        this.closeModal();
    }

    openModal() {
        const modal = document.getElementById('notification-modal');
        if (modal) {
            modal.style.display = 'block';
        }
    }

    closeModal() {
        const modal = document.getElementById('notification-modal');
        if (modal) {
            modal.style.display = 'none';
        }
    }
}

export default NotificationHandler;