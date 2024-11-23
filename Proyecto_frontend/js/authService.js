import ApiClient from './apiClient.js';
import LoguinRequestDto from './dtos/LoguinRequestDto.js';
import RegisterRequestDto from './dtos/RegisterRequestDto.js';
import config from './config.js'; // Importa la configuración
import cart from './cart.js';

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

        //marcamos el tiempo en que se ejecuta la funcion
        console.log('AuthService initialized at', new Date().toLocaleTimeString());

        this.token = localStorage.getItem('authToken');
        this.tokenExpiry = this.getExpiration();
        if (this.token && this.tokenExpiry) {
            console.log('Token found:', this.token);
            this.apiClient.token = this.token; // Actualiza el token en ApiClient
        } else {
            console.log('No token found, user is not authenticated.');
        }
    }

    /**
     * Inicializa el servicio de autenticación.
     * Intenta recuperar el token de autenticación y su fecha de expiración del localStorage.
     */
    init() {

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

    //devolvemo el token del usuario
    getToken() {
        //si el token esta vencido lo eliminamos y devoovemos null
        if (this.isTokenExpired()) {
            return null;
        }
        return this.token;
    }

    /**
     * Realiza el login del usuario.
     * Envía una solicitud POST al endpoint /api/login con el nombre de usuario y la contraseña.
     * Si la autenticación es exitosa, guarda el token y su fecha de expiración en localStorage.
     * 
     * @param {string} email - El nombre de usuario.
     * @param {string} password - La contraseña del usuario.
     * @returns {Promise<{success: boolean, message?: string}>} - Retorna una promesa que resuelve a un objeto con la propiedad success y opcionalmente message si hay errores.
     */
    async login(email, password) {
        try {
            // Creamos un dto con los datos del usuario
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
                    return { success: true };
                } else {
                    return { success: false, message: 'Login failed: token not found' };
                }
            } else if (response.status === 401) {
                return { success: false, message: 'Invalid credentials' };
            } else {
                return { success: false, message: `Unexpected status code: ${response.status}` };
            }
        } catch (error) {
            if(error.status === 401){
                return { success: false, message: 'Invalid credentials' };
            }else{
                return { success: false, message: error };
            }
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
        //borramos el token de la cahe
        this.authCache.isAuthenticated =false;
        this.authCache.expiry = 0;        
        this.apiClient.token = null; // Elimina el token en ApiClient
        try{
            cart.clearCart();
        }catch(error){
            console.error('Error clearing cart:', error);
        }
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
    
            // Calcular el tiempo restante del token
            const tokenExpiryTime = this.tokenExpiry - now;
            const cacheExpiryTime = Math.min(tokenExpiryTime, 5 * 60 * 1000); // Caché válida por el tiempo restante del token o 5 minutos, lo que sea menor
    
            // Actualizar la caché con el nuevo estado de autenticación y su tiempo de expiración
            this.authCache.isAuthenticated = isAuthenticated;
            this.authCache.expiry = now + cacheExpiryTime;
    
            return isAuthenticated;
        } catch (error) {
            return false;
        }
    }

    async getUserId() {
        try {
            const token = this.token;
            if (!token) {
                throw new Error('No token found');
            }

            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));

            const decodedToken = JSON.parse(jsonPayload);
            if (!decodedToken.id) {
                throw new Error('User ID not found in token');
            }
            const id = decodedToken.id;
            return id;
        } catch (error) {
            return null;
        }
    }

    async getExpiration() {
        try {
            const token = this.token;
            if (!token) {
                throw new Error('No token found');
            }

            const base64Url = token.split('.')[1];
            const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
            const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
                return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
            }).join(''));

            const decodedToken = JSON.parse(jsonPayload);
            if (!decodedToken.exp) {
                throw new Error('Expiration not found in token');
            }
            const expiration = new Date(decodedToken.exp * 1000);
            return expiration;
        } catch (error) {
            return null;
        }
    }

    async getRole() {
        try {
            const token = this.token;
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
            return role;
        } catch (error) {
            return null;
        }
    }
}

// Crea una instancia de ApiClient y AuthService
const apiClient = new ApiClient('/api');
const authService = new AuthService(apiClient);
export default authService;