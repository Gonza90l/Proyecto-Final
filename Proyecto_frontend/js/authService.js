export class AuthService {
    constructor() {
        this.token = null;
    }

    init() {
        this.token = localStorage.getItem('authToken');
        if (this.token) {
            console.log('Token found:', this.token);
        } else {
            console.log('No token found, user is not authenticated.');
        }
    }

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

    logout() {
        this.token = null;
        localStorage.removeItem('authToken');
    }

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

export const authService = new AuthService();