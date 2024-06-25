import json
import pytest
from flask_testing import TestCase
from app import app, mysql

class BaseTestCase(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SECRET_KEY'] = 'frank'
        app.config['MYSQL_HOST'] = 'localhost'
        app.config['MYSQL_USER'] = 'root'
        app.config['MYSQL_PASSWORD'] = ''
        app.config['MYSQL_DB'] = 'adn_telecom_test'  # Usar una base de datos de prueba
        return app

    def setUp(self):
        self.connection = mysql.connection
        self.cursor = self.connection.cursor()

    def tearDown(self):
        self.connection.rollback()  # Revertir cualquier cambio realizado durante las pruebas
        self.cursor.close()

class TestApp(BaseTestCase):
    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ADN Telecom', response.data)

    def test_login(self):
        # Añadir un usuario de prueba a la base de datos
        self.cursor.execute("INSERT INTO usuarios (nombre, correo, password, id_rol) VALUES (%s, %s, %s, %s)", 
                            ('Test User', 'test_user@example.com', 'test_password', 2))
        self.connection.commit()

        response = self.client.post('/acceso-login', data=dict(
            txtCorreo='test_user@example.com',
            txtPassword='test_password'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Usuario o contrase\xc3\xb1a incorrecta', response.data)

        # Limpiar la base de datos
        self.cursor.execute("DELETE FROM usuarios WHERE correo = 'test_user@example.com'")
        self.connection.commit()

    def test_register_user(self):
        response = self.client.post('/crear-registro', data=dict(
            txtNombre='Nuevo Usuario',
            txtCorreo='jonah@example.com',
            txtPassword='123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registro exitoso', response.data)

        # Limpiar la base de datos
        self.cursor.execute("DELETE FROM usuarios WHERE correo = 'user@example.com'")
        self.connection.commit()

    def test_register_existing_user(self):
        # Añadir un usuario de prueba a la base de datos
        self.cursor.execute("INSERT INTO usuarios (nombre, correo, password, id_rol) VALUES (%s, %s, %s, %s)",
                            ('Existing User', 'existing_user@example.com', 'password', 2))
        self.connection.commit()

        # Intentar registrar el mismo usuario
        response = self.client.post('/crear-registro', data=dict(
            txtNombre='Existing User',
            txtCorreo='existing_user@example.com',
            txtPassword='password'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'El correo ya est\xc3\xa1 registrado, elija otro.', response.data)

        # Limpiar la base de datos
        self.cursor.execute("DELETE FROM usuarios WHERE correo = 'existing_user@example.com'")
        self.connection.commit()

    def test_edit_user(self):
        # Añadir un usuario de prueba a la base de datos
        self.cursor.execute("INSERT INTO usuarios (nombre, correo, password, id_rol) VALUES (%s, %s, %s, %s)",
                            ('Edit User', 'edit_user@example.com', 'password', 2))
        self.connection.commit()
        user_id = self.cursor.lastrowid

        # Editar el usuario
        response = self.client.post(f'/modificar/{user_id}', data=dict(
            txtNombre='Edited User',
            txtCorreo='edited_user@example.com',
            txtPassword='new_password'
        ))
        self.assertEqual(response.status_code, 302)  # Redirect after success

        # Verificar los cambios
        self.cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
        user = self.cursor.fetchone()
        self.assertEqual(user['nombre'], 'Edited User')
        self.assertEqual(user['correo'], 'edited_user@example.com')

        # Limpiar la base de datos
        self.cursor.execute("DELETE FROM usuarios WHERE id = %s", (user_id,))
        self.connection.commit()

    def test_componentes_page(self):
        response = self.client.get('/componentes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Componentes', response.data)

    def test_add_component(self):
        response = self.client.post('/agregar_componente', data=dict(
            EQUIPO='Test Equipo',
            MODELO='Test Modelo',
            MARCA='Test Marca',
            COSTO=100,
            Velocidad_Red=1000,
            Year=2022,
            Estructura_Red=1,
            Nro_Puertos=4,
            descripcion='Test Descripcion',
            Imagen='https://example.com/image.jpg'
        ))
        self.assertEqual(response.status_code, 302)  # Redirect after success

        self.cursor.execute("SELECT * FROM componentes WHERE EQUIPO = 'Test Equipo'")
        component = self.cursor.fetchone()
        self.assertIsNotNone(component)
        self.assertEqual(component['MODELO'], 'Test Modelo')

        # Limpiar la base de datos
        self.cursor.execute("DELETE FROM componentes WHERE EQUIPO = 'Test Equipo'")
        self.connection.commit()

if __name__ == '__main__':
    pytest.main()