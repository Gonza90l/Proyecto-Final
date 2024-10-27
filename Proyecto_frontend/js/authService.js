// AuthService
// Tipo de instancia: Singleton

/**
 * AuthService es una clase que maneja la autenticación del usuario.
 * Utiliza el patrón Singleton para asegurar que solo haya una instancia de la clase.
 */
class AuthService {

    constructor() {
        // Inicializa el token y la fecha de expiración a null
        this.token = null;
        this.tokenExpiry = null;
    }

    /**
     * Inicializa el servicio de autenticación.
     * Intenta recuperar el token de autenticación y su fecha de expiración del localStorage.
     */
    init() {
        this.token = localStorage.getItem('authToken');
        this.tokenExpiry = localStorage.getItem('tokenExpiry');
        if (this.token && this.tokenExpiry) {
            console.log('Token found:', this.token);
        } else {
            console.log('No token found, user is not authenticated.');
        }
    }

    /**
     * Realiza el login del usuario.
     * Envía una solicitud POST al endpoint /api/login con el nombre de usuario y la contraseña.
     * Si la autenticación es exitosa, guarda el token y su fecha de expiración en localStorage.
     * 
     * @param {string} username - El nombre de usuario.
     * @param {string} password - La contraseña del usuario.
     * @returns {Promise<boolean>} - Retorna una promesa que resuelve a true si el login es exitoso, de lo contrario lanza un error.
     */
    async login(username, password) {
        return fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.token && data.expiresIn) {
                this.token = data.token;
                this.tokenExpiry = Date.now() + data.expiresIn * 1000; // Convertir segundos a milisegundos
                localStorage.setItem('authToken', this.token);
                localStorage.setItem('tokenExpiry', this.tokenExpiry);
                return true;
            } else {
                throw new Error('Login failed');
            }
        });
    }

    /**
     * Realiza el logout del usuario.
     * Elimina el token de autenticación y su fecha de expiración del localStorage y los establece a null.
     */
    logout() {
        this.token = null;
        this.tokenExpiry = null;
        localStorage.removeItem('authToken');
        localStorage.removeItem('tokenExpiry');
    }

    /**
     * Verifica si el token ha expirado localmente.
     * 
     * @returns {boolean} - Retorna true si el token ha expirado, de lo contrario false.
     */
    isTokenExpired() {
        return Date.now() > this.tokenExpiry;
    }

    /**
     * Verifica si el usuario está autenticado.
     * Primero verifica si el token ha expirado localmente.
     * Si no ha expirado, considera que el usuario está autenticado.
     * 
     * @returns {Promise<boolean>} - Retorna una promesa que resuelve a true si el token es válido, de lo contrario resuelve a false.
     */
    async isAuthenticated() {
        if (!this.token || this.isTokenExpired()) {
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