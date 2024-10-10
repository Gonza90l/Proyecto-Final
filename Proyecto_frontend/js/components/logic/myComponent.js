// components/logic/my-component.js
import { BaseComponent } from './baseComponent.js';

class MyComponent extends BaseComponent {
    constructor() {
        super('/components/views/myComponent.html');
    }
}

customElements.define('my-component', MyComponent);