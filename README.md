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

## Instrucciones de Instalación

### Clonar el Repositorio
Para clonar el repo, ejecuta este comando en la terminal:

```bash
git clone https://github.com/Gonza90l/Proyecto-Final.git
```

### Requisitos Previos
- Python 3.x
- pip (gestor de paquetes de Python)

### Instalación de Dependencias
Para instalar las dependencias necesarias, ejecuta este comando en la terminal desde la raíz del proyecto:

```bash
pip install -r Proyecto_backend/src/requirements.txt
```

### Configuración de Certificados SSL para HTTPS
Para configurar los certificados SSL, sigue estos pasos:

1. **Certificados Existentes**: Si ya tienes certificados SSL, colócalos en las carpetas adecuadas dentro del proyecto. Por ejemplo:
    - `Proyecto_backend/src/flaskr/ssl/cert.pem`
    - `Proyecto_backend/src/flaskr/ssl/key.pem`

2. **Crear Certificados SSL**: Si no tienes certificados SSL, puedes crearlos usando la consola. Ejecuta este comando para generar un certificado autofirmado:

    ```bash
    openssl req -x509 -nodes -days 3650 -newkey rsa:4096 -keyout Proyecto_backend/src/flaskr/ssl/key.pem -out Proyecto_backend/src/flaskr/ssl/cert.pem
    ```

    Sigue las instrucciones en pantalla para completar la generación del certificado.

### Configuración del Archivo .env

Para configurar el archivo `.env`, sigue estos pasos:

1. **Copiar el archivo `.env_example`**: copia el archivo `.env_example` y renómbralo a `.env`. Puedes hacerlo con este comando en la terminal desde la raíz del proyecto:

    ```bash
    cp .env_example .env
    ```

2. **Editar el archivo `.env`**: Abre el archivo `.env` en tu editor de texto favorito y completa los valores necesarios. A continuación, un ejemplo de cómo debería verse el archivo `.env`:

    ```plaintext
    # .env
    FLASK_ENV=development
    SECRET_KEY="tu_clave_secreta"

    # Database
    MYSQL_HOST=localhost
    MYSQL_PORT=3306
    MYSQL_USER=root
    MYSQL_PASSWORD=
    MYSQL_DB=proyecto_informatico
    MYSQL_CURSORCLASS=DictCursor

    # Si usas flask-mysqldb pon en true, si no, usa mysql-connector-python
    # flask-mysqldb no permite conectarse sin TLS a la base de datos, así que 
    # usa mysql-connector-python si la base de datos no tiene TLS
    USE_FLASK_MYSQLDB=true

    # CORS
    CORS_ORIGINS=https://proyecto_frontend.test
    CORS_METHODS=GET,POST,PUT,DELETE
    CORS_ALLOW_HEADERS=Content-Type,Authorization

    # SSL
    SSL_CERTFILE=./flaskr/ssl/cert.pem
    SSL_KEYFILE=./flaskr/ssl/key.pem
    ```

Asegúrate de reemplazar `"tu_clave_secreta"` con una clave segura y de completar cualquier otra variable según sea necesario para tu entorno.

Si usas XAMPP, pon USE_FLASK_MYSQLDB=false, ya que se genera error por el uso de TLS durante la conexión.

### Configuración de la Base de Datos

Para levantar la infraestructura de la base de datos, sigue estos pasos:

1. **Navegar a la Carpeta de Configuración de la Base de Datos**:
    - Ubicación: `Proyecto_backend/documentation/database_settings`

2. **Crear la Base de Datos**:
    - Ejecuta el script `create_db.sql` para crear la base de datos y las tablas necesarias. Puedes hacerlo desde la línea de comandos de MySQL o usando una herramienta de administración de bases de datos como phpMyAdmin.

    ```sql
    source Proyecto_backend/documentation/database_settings/create_db.sql;
    ```

3. **Verificar la Creación de la Base de Datos**:
    - Asegúrate de que la base de datos y las tablas se hayan creado correctamente verificando en tu herramienta de administración de bases de datos.

Una vez completados estos pasos, la infraestructura de la base de datos estará lista para ser utilizada por la aplicación.

### Ejecución de la Aplicación
Una vez instaladas las dependencias y configurados los certificados SSL, puedes ejecutar la aplicación con el siguiente comando desde la raíz del proyecto:

```bash
python Proyecto_backend/src/run.py
```

La aplicación estará disponible en `https://localhost:5000`.

### Ejecución del frontend

Para ejecutar el frontend, es necesario cargarlo desde un servidor web como Apache, ya que utiliza JavaScript para el enrutamiento y debe ser servido desde la web. Sigue estos pasos para configurar y ejecutar el frontend:

1. **Iniciar Apache**:
    - Asegúrate de que Apache esté corriendo en XAMPP. Puedes hacerlo desde el Panel de Control de XAMPP.

2. **Acceder al Frontend**:
    - Una vez que Apache esté corriendo, abre tu navegador web y navega a `http://proyecto_frontend.test` para acceder a la aplicación frontend.

Recuerda que el frontend debe estar ubicado en la carpeta `C:/xampp/htdocs/proyecto_frontend` para que Apache pueda servirlo correctamente. También puedes crear un virtualHost en Apache y establecer el DocumentRoot a la carpeta donde tengas el proyecto, por ejemplo:

```plaintext
C:/Users/tu_usuario/UPSO/Proyecto_final/proyecto_frontend
```

### Configuración de un Virtual Host en XAMPP

Para configurar un Virtual Host en XAMPP y modificar el archivo `hosts` para acceso local, sigue estos pasos:

#### Configurar el Virtual Host en XAMPP

1. **Abrir el archivo `httpd-vhosts.conf`**:
    - Ubicación típica: `C:\xampp\apache\conf\extra\httpd-vhosts.conf`
    - Abre el archivo en tu editor de texto favorito.

2. **Agregar la configuración del Virtual Host**:
    - Añade la siguiente configuración al final del archivo:

    ```apache
    <VirtualHost *:80>
        ServerAdmin webmaster@proyecto.test
        DocumentRoot "C:/xampp/htdocs/proyecto_frontend"
        ServerName proyecto_frontend.test
        ErrorLog "logs/proyecto_frontend-error.log"
        CustomLog "logs/proyecto_frontend-access.log" common
        <Directory "C:/xampp/htdocs/proyecto_frontend">
            Options Indexes FollowSymLinks Includes ExecCGI
            AllowOverride All
            Require all granted
        </Directory>
    </VirtualHost>
    ```

    ```apache
    <VirtualHost *:443>
        ServerAdmin webmaster@proyecto.test
        DocumentRoot "C:/xampp/htdocs/proyecto_frontend"
        ServerName proyecto_frontend.test
        ErrorLog "logs/proyecto_frontend-ssl-error.log"
        CustomLog "logs/proyecto_frontend-ssl-access.log" common
        SSLEngine on
        SSLCertificateFile "C:/xampp/apache/conf/ssl.crt/server.crt"
        SSLCertificateKeyFile "C:/xampp/apache/conf/ssl.key/server.key"
        <Directory "C:/xampp/htdocs/proyecto_frontend">
            Options Indexes FollowSymLinks Includes ExecCGI
            AllowOverride All
            Require all granted
        </Directory>
    </VirtualHost>
    ```
    - Asegúrate de ajustar las rutas según la ubicación del proyecto.

#### Modificar el Archivo `hosts`

1. **Abrir el archivo `hosts`**:
    - Ubicación típica: `C:\Windows\System32\drivers\etc\hosts`
    - Abre el archivo en tu editor de texto favorito con permisos de administrador.

2. **Agregar la entrada del Virtual Host**:
    - Añade la siguiente línea al final del archivo:

    ```plaintext
    127.0.0.1 proyecto_frontend.test
    ```

Con esto ya podrías ejecutar de manera local el proyecto bajo SSL y un dominio de prueba.

#### Reiniciar Apache

1. **Reiniciar el servidor Apache**:
    - Abre el Panel de Control de XAMPP.
    - Detén y luego inicia nuevamente el módulo Apache.

Una vez completados estos pasos, deberías poder acceder a tu aplicación en `http://proyecto_frontend.test`.

