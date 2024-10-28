export class ApiClient {
    constructor(baseURL, token = null) {
        this.baseURL = baseURL;
        this.token = token;
        this.maxRetries = 3; // Número máximo de reintentos en caso de fallo
    }

    _getHeaders(contentType = 'application/json') {
        const headers = {
            'Content-Type': contentType
        };
        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }
        return headers;
    }

    async _fetchWithRetry(url, options, retries = this.maxRetries) {
        try {
            const response = await fetch(url, options);
            if (response.status === 401) {
                console.error('Token expired or invalid');
            }
            return await this._handleResponse(response);
        } catch (error) {
            if (retries > 0 && (error.name === 'TypeError' || error.message === 'Failed to fetch')) {
                console.warn(`Retrying... (${this.maxRetries - retries + 1}/${this.maxRetries})`);
                return await this._fetchWithRetry(url, options, retries - 1);
            } else {
                console.error('Failed after maximum retries');
                throw error;
            }
        }
    }

    async get(endpoint) {
        return this._fetchWithRetry(`${this.baseURL}${endpoint}`, {
            headers: this._getHeaders()
        });
    }

    async post(endpoint, data) {
        return this._fetchWithRetry(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers: this._getHeaders(),
            body: JSON.stringify(data)
        });
    }

    async put(endpoint, data) {
        return this._fetchWithRetry(`${this.baseURL}${endpoint}`, {
            method: 'PUT',
            headers: this._getHeaders(),
            body: JSON.stringify(data)
        });
    }

    async patch(endpoint, data) {
        return this._fetchWithRetry(`${this.baseURL}${endpoint}`, {
            method: 'PATCH',
            headers: this._getHeaders(),
            body: JSON.stringify(data)
        });
    }

    async delete(endpoint) {
        return this._fetchWithRetry(`${this.baseURL}${endpoint}`, {
            method: 'DELETE',
            headers: this._getHeaders()
        });
    }

    async _handleResponse(response) {
        const contentType = response.headers.get('content-type');
        let data;

        if (contentType && contentType.includes('application/json')) {
            data = await response.json();
            //si exiiste el campo data en la respuesta, lo devolvemos
            if (data.data) {
                data = data.data;
            }
        } else {
            data = await response.text();
        }

        if (!response.ok) {
            const error = {
                status: response.status,
                data: data,
                error: response.statusText
            };
            throw error;
        }

        return {
            status: response.status,
            data: data
        };
    }

    setToken(newToken) {
        this.token = newToken;
    }
}

export default ApiClient;