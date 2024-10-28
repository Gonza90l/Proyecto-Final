import ApiClient from './apiClient.js';
// AuthService
// Tipo de instancia: Singleton

/**
 * AuthService es una clase que maneja la autenticación del usuario.
 * Utiliza el patrón Singleton para asegurar que solo haya una instancia de la clase.
 */
class AuthService {

    constructor() {
        // Inicializa el token y la fecha de expiración a null
        this.apiClient = new ApiClient('https://proyecto_frontend.test:5000');
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
            this.apiClient.token = this.token; // Actualiza el token en ApiClient
        } else {
            console.log('No token found, user is not authenticated.');
        }
    }

    /**
     * Realiza el login del usuario.
     * Envía una solicitud POST al endpoint /api/login con el nombre de usuario y la contraseña.
     * Si la autenticación es exitosa, guarda el token y su fecha de expiración en localStorage.
     * 
     * @param {string} email - El nombre de usuario.
     * @param {string} password - La contraseña del usuario.
     * @returns {Promise<boolean>} - Retorna una promesa que resuelve a true si el login es exitoso, de lo contrario lanza un error.
     */
    async login(email, password) {
        try {
            const response = await this.apiClient.post('/login', { email, password });

            // Verificamos el código de estado antes de llamar a response.json()
            if (response.status === 200) {
                const apiResponse = response.data; // Obtener los datos JSON de la respuesta
                if (apiResponse.token) {
                    this.token = apiResponse.token;
                    this.tokenExpiry = Date.now() + apiResponse.expiresIn * 1000; // Convertir segundos a milisegundos
                    localStorage.setItem('authToken', this.token);
                    localStorage.setItem('tokenExpiry', this.tokenExpiry);
                    this.apiClient.token = this.token; // Actualiza el token en ApiClient
                    return true;
                } else {
                    throw new Error('Login failed: token not found');
                }
            } else if (response.status === 401) {
                console.error('Invalid credentials');
                return false;
            } else {
                console.error('Unexpected status code:', response.status); // Error desconocido
                throw new Error('Login failed');
            }
        } catch (error) {
            console.error('Login error:', error);
            return false;
        }
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
        this.apiClient.token = null; // Elimina el token en ApiClient
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
            const data = await this.apiClient.post('/verify_token', {});
            // Si la respuesta es exitosa, el token es válido
            console.log('Token verification:', data);
            return data.status === 200;
        } catch (error) {
            console.error('Token verification failed:', error);
            return false;
        }
    }
}

// Crea una instancia de ApiClient y AuthService
const apiClient = new ApiClient('/api');
const authService = new AuthService(apiClient);
export default authService;