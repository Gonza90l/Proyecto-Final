# Proyecto Grupal - Sistema para Pedidos de Comidas

## Asignatura: Proyecto Informático

### Descripción General

Este proyecto tiene como objetivo desarrollar un **Sistema para Pedidos de Comidas** que funcione en base a una **API RESTful** y un **cliente web**. El sistema permitirá a los usuarios gestionar menús, realizar pedidos, consultar estados y mantener un historial de los pedidos. Los administradores podrán gestionar los menús y los pedidos de los usuarios.

### Perfiles de Usuarios
- **Usuario**: Puede visualizar el menú, crear pedidos, consultar su estado, actualizar o cancelar pedidos, ver su historial, y dejar comentarios y valoraciones sobre los platos.
- **Administrador**: Puede gestionar el menú (crear, modificar, eliminar platos), y gestionar los pedidos (consultar y modificar su estado).

## Características Principales

### Gestión del Menú:
- Visualización de los platos con nombre, descripción, precio, e imagen (opcional).
- Clasificación de platos en categorías (ej. entradas, platos principales, postres).
- Los administradores pueden **crear, modificar y eliminar** platos del menú.

### Gestión de Pedidos:
- Los usuarios pueden **crear un pedido** seleccionando varios platos del menú.
- Cada pedido incluye: lista de platos, cantidad, precio total, fecha y hora del pedido.
- Los usuarios pueden **consultar el estado** de su pedido (pendiente, en preparación, enviado, entregado).
- Los usuarios pueden **actualizar o cancelar** su pedido antes de que entre en preparación.
- Los administradores pueden **consultar y modificar el estado** de los pedidos de todos los usuarios.

### Historial de Pedidos:
- Los usuarios pueden **consultar su historial de pedidos** anteriores con detalles como lista de platos, fecha, precio y estado final.

### Otras Funcionalidades:
- **Notificaciones**: Los usuarios reciben notificaciones cuando cambia el estado de su pedido.
- **Manejo de Pagos**: Se integra una funcionalidad básica para pagos (tarjetas u otro método).
- **Comentarios y Valoraciones**: Los usuarios pueden dejar comentarios y valoraciones sobre los platos recibidos.

## Tecnologías Utilizadas

### Backend
- **Lenguaje**: Python
- **Framework**: Flask
- **Base de datos**: SQL (por definir)
- **API**: RESTful (formato de intercambio de datos en JSON)

### Frontend
- **Lenguajes**: HTML, CSS, JavaScript
- **Cliente Web**: Diseño responsivo para dispositivos móviles y pantallas de escritorio.

### Control de Versiones
- **Sistema de control**: Git
- **Repositorio**: El repositorio inicial es creado por el Project Manager y los demás miembros del equipo son añadidos como colaboradores.
