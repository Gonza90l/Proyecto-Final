import ApiClient from './apiClient.js';
import LoguinRequestDto from './dtos/LoguinRequestDto.js';
import RegisterRequestDto from './dtos/RegisterRequestDto.js';
import config from './config.js'; // Importa la configuración


// AuthService
// Tipo de instancia: Singleton

/**
 * AuthService es una clase que maneja la autenticación del usuario.
 * Utiliza el patrón Singleton para asegurar que solo haya una instancia de la clase.
 */
class AuthService {

    constructor() {
        // Inicializa el token y la fecha de expiración a null
        this.apiClient = new ApiClient(config.apiBaseUrl);
        this.token = null;
        this.authCache = {
            isAuthenticated: false,
            expiry: 0
        };
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
     * Realiza el registro de un nuevo usuario.
     * Envía una solicitud POST al endpoint /api/register con el correo electrónico, la contraseña, el nombre y el apellido del usuario.
     * 
     * @param {string} email - El correo electrónico del usuario.
     * @param {string} password - La contraseña del usuario.
     * @param {string} name - El nombre del usuario.
     * @param {string} lastname - El apellido del usuario.
     * 
     * @returns {Promise<{success: boolean, error?: object}>} - Retorna una promesa que resuelve a un objeto con la propiedad success y opcionalmente error si hay errores.
     */
    async register(email, password, name, lastname) {
        try {
            const registerRequestDto = new RegisterRequestDto(email, password, name, lastname);
    
            const response = await this.apiClient.post('/register', registerRequestDto);
    
            if (response.status !== 200) {
                console.error('Register error 1:', response.data);
                // si existe el campo error en la respuesta, lo devolvemos
                if (response.data.errors) {
                    return { success: false, error: response.data.errors };
                }
                return { success: false, error: response.data };
            }
    
            return { success: true };
    
        } catch (error) {
            // si existe el campo error en la respuesta, lo devolvemos
            if (error.data.errors) {
                return { success: false, error: error.data.errors };
            }
            return { success: false, error: error };
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
            // creamnos un dto con los datos del usuario
            const loguinRequestDto = new LoguinRequestDto(email, password);

            const response = await this.apiClient.post('/login', loguinRequestDto);

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
        const now = Date.now();

        if (!this.token || this.isTokenExpired()) {
            return false;
        }

        // Verificar si el estado de autenticación está en caché y no ha expirado
        if (this.authCache.expiry > now) {
            return this.authCache.isAuthenticated;
        }

        try {
            const data = await this.apiClient.post('/verify_token', {});
            // Si la respuesta es exitosa, el token es válido
            const isAuthenticated = data.status === 200;
            console.log('Token verification:', data);

            // Actualizar la caché con el nuevo estado de autenticación y su tiempo de expiración
            this.authCache.isAuthenticated = isAuthenticated;
            this.authCache.expiry = now + 5 * 60 * 1000; // Caché válida por 5 minutos

            return isAuthenticated;
        } catch (error) {
            console.error('Token verification failed:', error);
            return false;
        }
    }

    async getRole() {
        try {
            const token = localStorage.getItem('authToken');
            if (!token) {
                throw new Error('No token found');
            }

            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));

            const decodedToken = JSON.parse(jsonPayload);
            if (!decodedToken.role) {
                throw new Error('Role not found in token');
            }
            const role = decodedToken.role.toLowerCase();
            console.log('Role:', role);
            return role;
        } catch (error) {
            console.error('Error getting role:', error);
            return null;
        }
    }
}

// Crea una instancia de ApiClient y AuthService
const apiClient = new ApiClient('/api');
const authService = new AuthService(apiClient);
export default authService;