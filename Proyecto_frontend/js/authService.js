// AuthService
// Tipo de instancia: Singleton

/**
 * AuthService es una clase que maneja la autenticación del usuario.
 * Utiliza el patrón Singleton para asegurar que solo haya una instancia de la clase.
 */
class AuthService {

    constructor() {
        // Inicializa el token a null
        this.token = null;
    }

    /**
     * Inicializa el servicio de autenticación.
     * Intenta recuperar el token de autenticación del localStorage.
     */
    init() {
        this.token = localStorage.getItem('authToken');
        if (this.token) {
            console.log('Token found:', this.token);
        } else {
            console.log('No token found, user is not authenticated.');
        }
    }

    /**
     * Realiza el login del usuario.
     * Envía una solicitud POST al endpoint /api/login con el nombre de usuario y la contraseña.
     * Si la autenticación es exitosa, guarda el token en localStorage.
     * 
     * @param {string} username - El nombre de usuario.
     * @param {string} password - La contraseña del usuario.
     * @returns {Promise<boolean>} - Retorna una promesa que resuelve a true si el login es exitoso, de lo contrario lanza un error.
     */
    login(username, password) {
        return fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                this.token = data.token;
                localStorage.setItem('authToken', this.token);
                return true;
            } else {
                throw new Error('Login failed');
            }
        });
    }

    /**
     * Realiza el logout del usuario.
     * Elimina el token de autenticación del localStorage y lo establece a null.
     */
    logout() {
        this.token = null;
        localStorage.removeItem('authToken');
    }

    /**
     * Verifica si el usuario está autenticado.
     * Envía una solicitud POST al endpoint /api/verify-token con el token de autenticación.
     * 
     * @returns {Promise<boolean>} - Retorna una promesa que resuelve a true si el token es válido, de lo contrario resuelve a false.
     */
    async isAuthenticated() {
        if (!this.token) {
            return false;
        }

        try {
            const response = await fetch('/api/verify-token', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${this.token}`
                }
            });

            if (!response.ok) {
                throw new Error('Token verification failed');
            }

            const data = await response.json();
            return data.valid;
        } catch (error) {
            console.error('Token verification failed:', error);
            return false;
        }
    }
}

// Crea una instancia única de AuthService y la exporta
const authService = new AuthService();
export default authService;