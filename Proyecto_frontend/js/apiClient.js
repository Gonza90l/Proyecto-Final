// Tipo de instancia: Transient (cada vez que se instancia se crea una nueva instancia)

export class ApiClient {
    constructor(baseURL, token) {
        this.baseURL = baseURL;
        this.token = token;
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

    async get(endpoint) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            headers: this._getHeaders()
        });
        return this._handleResponse(response);
    }

    async post(endpoint, data) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'POST',
            headers: this._getHeaders(),
            body: JSON.stringify(data)
        });
        return this._handleResponse(response);
    }

    async put(endpoint, data) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'PUT',
            headers: this._getHeaders(),
            body: JSON.stringify(data)
        });
        return this._handleResponse(response);
    }

    async delete(endpoint) {
        const response = await fetch(`${this.baseURL}${endpoint}`, {
            method: 'DELETE',
            headers: this._getHeaders()
        });
        return this._handleResponse(response);
    }

    async _handleResponse(response) {
        if (!response.ok) {
            const error = await response.text();
            throw new Error(error);
        }

        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return response.json();
        } else {
            return response.text();
        }
    }
}