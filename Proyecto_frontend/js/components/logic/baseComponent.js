// components/logic/base-component.js
export class BaseComponent extends HTMLElement {
    constructor(templatePath) {
        super();
        this.templatePath = templatePath;
        this.attachShadow({ mode: 'open' });
    }

    async connectedCallback() {
        try {
            const template = await this.loadTemplate();
            this.shadowRoot.appendChild(template.content.cloneNode(true));
        } catch (error) {
            console.error('Error loading template:', error);
        }
    }

    async loadTemplate() {
        try {
            const response = await fetch(this.templatePath);
            if (!response.ok) {
                throw new Error(`Failed to load template: ${response.statusText}`);
            }
            const text = await response.text();
            const template = document.createElement('template');
            template.innerHTML = text;
            return template;
        } catch (error) {
            console.error('Error fetching template:', error);
            throw error;
        }
    }
}