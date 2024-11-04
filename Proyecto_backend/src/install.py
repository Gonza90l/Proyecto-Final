import os
import subprocess
import ctypes
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Verificar si el script se está ejecutando con permisos de administrador
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Instalar dependencias desde requirements.txt
def install_requirements():
    print("Instalando dependencias...")
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if not os.path.exists(requirements_path):
        raise FileNotFoundError(f"El archivo {requirements_path} no existe.")
    try:
        subprocess.check_call(['pip', 'install', '-r', requirements_path])
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar dependencias: {e}. Continuando con el script...")

# Generar y guardar la clave única de la aplicación
def generate_and_save_secret_key():
    print("Generando clave secreta...")
    import os
    import secrets

    # Leer el archivo .env si existe
    env_file_path = '.env'
    secret_key = None

    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as env_file:
            lines = env_file.readlines()
            for line in lines:
                if line.startswith('SECRET_KEY='):
                    secret_key = line.strip().split('=')[1]
                    break

    # Si no existe la clave secreta, generarla y guardarla
    if not secret_key:
        print("Generando clave secreta...")
        secret_key = secrets.token_hex(32)
        with open(env_file_path, 'a') as env_file:
            env_file.write(f'\nSECRET_KEY={secret_key}\n')

    # Actualizar la variable de entorno
    os.environ['SECRET_KEY'] = secret_key

def create_ssl_certificates():
    print("Creando certificados SSL...")
    from OpenSSL import crypto
    from os import environ
    ssl_dir = 'proyecto_backend/ssl'
    os.makedirs(ssl_dir, exist_ok=True)

    key_file = os.path.join(ssl_dir, 'key.pem')
    cert_file = os.path.join(ssl_dir, 'cert.pem')

    # Crear clave y certificado
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    cert = crypto.X509()
    cert.get_subject().C = "AR"
    cert.get_subject().ST = "Buenos Aires"
    cert.get_subject().L = "Monte Hermoso"
    cert.get_subject().O = "UPSO"
    cert.get_subject().OU = "Proyecto informatico"
    cert.get_subject().CN = "localhost"
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, 'sha256')

    with open(cert_file, 'wb') as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open(key_file, 'wb') as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))


# Configurar la base de datos
def setup_database():
    print("Configurando base de datos...")
    from werkzeug.security import generate_password_hash
    import os
    import time

    db_name = os.getenv('MYSQL_DB')
    db_user = os.getenv('MYSQL_USER')
    db_password = os.getenv('MYSQL_PASSWORD')
    db_host = os.getenv('MYSQL_HOST')
    db_port = os.getenv('MYSQL_PORT', '3306')  # Proporcionar un valor predeterminado para MYSQL_PORT
    use_flask_mysqldb = os.getenv('USE_FLASK_MYSQLDB', 'false').lower() == 'true'

    while True:
        try:
            if use_flask_mysqldb:
                import MySQLdb
                conn = MySQLdb.connect(
                    user=db_user,
                    passwd=db_password,
                    host=db_host,
                    port=int(db_port)
                )
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                cursor.execute(f"USE {db_name}")
            else:
                import mysql.connector
                conn = mysql.connector.connect(
                    user=db_user,
                    password=db_password,
                    host=db_host,
                    port=int(db_port)
                )
                cursor = conn.cursor()
                cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
                conn.database = db_name

            # Ejecutar scripts SQL para configurar la base de datos
            sql_files = ['../documentation/database_settings/create_db.sql', '../documentation/database_settings/crete_tables.sql']
            for sql_file in sql_files:
                print(f"Ejecutando {sql_file}...")
                with open(sql_file, 'r') as file:
                    sql_statements = file.read().split(';')
                    for statement in sql_statements:
                        if statement.strip():
                            cursor.execute(statement)

            # Preguntar por los detalles del administrador
            admin_name = input("Ingrese el nombre del administrador: ")
            admin_lastname = input("Ingrese el apellido del administrador: ")
            admin_username = input("Ingrese el email de usuario del administrador: ")
            admin_password = input("Ingrese la contraseña del administrador: ")
            app_key = os.getenv('SECRET_KEY')

            # Encriptar la contraseña
            hashed_password = generate_password_hash(admin_password)

            # Insertar el usuario administrador en la base de datos
            cursor.execute(
                "INSERT INTO user (name, lastname, email, password, role) VALUES (%s, %s, %s, %s, %s)",
                (admin_name, admin_lastname, admin_username, hashed_password, 'ADMIN')
            )

            conn.commit()
            cursor.close()
            conn.close()

            # Actualizar el archivo .env con el nombre de la base de datos
            update_env_variable('MYSQL_DB', db_name)
            break

        except MySQLdb.OperationalError as e:
            print(f"Error de conexión a la base de datos: {e}")
            print("Por favor, asegúrese de que el servidor MySQL esté en funcionamiento y las credenciales sean correctas.")
            retry = input("¿Desea reintentar la operación? (sí/no): ").strip().lower()
            if retry not in ['sí', 'si', 'yes', 'y', 's']:
                break
            time.sleep(5)  # Esperar 5 segundos antes de reintentar

        except mysql.connector.Error as e:
            print(f"Error de conexión a la base de datos: {e}")
            print("Por favor, asegúrese de que el servidor MySQL esté en funcionamiento y las credenciales sean correctas.")
            retry = input("¿Desea reintentar la operación? (sí/no): ").strip().lower()
            if retry not in ['sí', 'si', 'yes', 'y', 's']:
                break
            time.sleep(5)  # Esperar 5 segundos antes de reintentar

def register_virtual_host(domain):
    print("Registrando virtual host...")
    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '../../Proyecto_frontend')
    ).replace('\\', '/')

    # Imprimir la ruta para verificar
    print(f"Ruta del proyecto: \"{project_root}\"")

    vhost_config_template_laragon = """
Define ROOT "{project_root}"
Define SITE "{domain}"

<VirtualHost *:80>
    DocumentRoot "${{ROOT}}"
    ServerName ${{SITE}}
    ServerAlias *.${{SITE}}
    <Directory "${{ROOT}}">
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>

<VirtualHost *:443>
    DocumentRoot "${{ROOT}}"
    ServerName ${{SITE}}
    ServerAlias *.${{SITE}}
    <Directory "${{ROOT}}">
        AllowOverride All
        Require all granted
    </Directory>

    SSLEngine on
    SSLCertificateFile "C:/laragon/etc/ssl/laragon.crt"
    SSLCertificateKeyFile "C:/laragon/etc/ssl/laragon.key"
</VirtualHost>
"""

    vhost_config_template_xampp = """
<VirtualHost *:80>
    DocumentRoot "{project_root}"
    ServerName {domain}
    ServerAlias *.{domain}
    <Directory "{project_root}">
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>

<VirtualHost *:443>
    DocumentRoot "{project_root}"
    ServerName {domain}
    ServerAlias *.{domain}
    <Directory "{project_root}">
        AllowOverride All
        Require all granted
    </Directory>

    SSLEngine on
    SSLCertificateFile "C:/xampp/apache/conf/ssl.crt/server.crt"
    SSLCertificateKeyFile "C:/xampp/apache/conf/ssl.key/server.key"
</VirtualHost>
"""

    if os.name == 'nt':  # Windows
        xampp_vhost_path = 'C:\\xampp\\apache\\conf\\extra\\httpd-vhosts.conf'
        laragon_vhost_dir = 'C:\\laragon\\etc\\apache2\\sites-enabled'

        if os.path.exists(xampp_vhost_path):
            with open(xampp_vhost_path, 'a', encoding='utf-8') as f:
                f.write(vhost_config_template_xampp.format(
                    project_root=project_root,
                    domain=domain
                ))
        elif os.path.exists(laragon_vhost_dir):
            laragon_vhost_path = os.path.join(laragon_vhost_dir, f'{domain}.conf')
            with open(laragon_vhost_path, 'w', encoding='utf-8') as f:
                f.write(vhost_config_template_laragon.format(
                    project_root=project_root,
                    domain=domain
                ))

        # Agregar entrada al archivo de hosts
        if is_admin():
            hosts_path = 'C:\\Windows\\System32\\drivers\\etc\\hosts'
            entries = [
                f'127.0.0.1 {domain}',
                '127.0.0.1 localhost',
                '::1 localhost'
            ]
            comment = '# Añadido automáticamente por el script de instalación de Proyecto Final'
            
            with open(hosts_path, 'r', encoding='utf-8') as f:
                existing_lines = f.readlines()

            with open(hosts_path, 'a', encoding='utf-8') as f:
                if comment not in ''.join(existing_lines):
                    f.write(f'\n{comment}\n')
                for entry in entries:
                    if entry not in existing_lines:
                        f.write(entry + '\n')

            print(f'Virtual host para {domain} ha sido registrado exitosamente.')
        else:
            print("No se pudo registrar el dominio en Hosts, ya que el script no se ejecutó con permisos de administrador.")

def update_env_variable(key, value):
    print(f"Actualizando variable de entorno {key}...")
    env_file_path = '.env'
    if os.path.exists(env_file_path):
        with open(env_file_path, 'r') as env_file:
            lines = env_file.readlines()

        with open(env_file_path, 'w') as env_file:
            for line in lines:
                if line.startswith(f'{key}='):
                    env_file.write(f'{key}={value}\n')
                else:
                    env_file.write(line)
            if not any(line.startswith(f'{key}=') for line in lines):
                env_file.write(f'{key}={value}\n')

# Actualizar la variable de entorno CORS_ORIGINS con el dominio proporcionado
def update_env_with_domain(domain):
    print("Actualizando variable de entorno...")
    cors_origins_value = f'https://{domain},http://{domain},http://localhost,https://localhost,http://127.0.0.1,https://127.0.0.1'
    update_env_variable('CORS_ORIGINS', cors_origins_value)

if __name__ == '__main__':
    domain = input("Ingrese el dominio en el que se ejecutará la app (e.g., localhost, proyecto_frontend.test): ").strip().lower()
    update_env_with_domain(domain)
    install_requirements()
    try:
        # Importar módulos después de instalar los requisitos
        from werkzeug.security import generate_password_hash
        from OpenSSL import crypto, SSL

        generate_and_save_secret_key()
        create_ssl_certificates()
        setup_database()
        register_virtual_host(domain)
        print("Instalación completada. Por favor, agregue manualmente la siguiente entrada al archivo de hosts:")
        print(f"127.0.0.1 {domain}")

        print ("Para ejecutar el servidor, ejecute el siguiente comando:")
        print ("python run.py")

    except ModuleNotFoundError as e:
        print(f"Error al importar módulos: {e}. Asegúrese de que todas las dependencias estén instaladas.")
