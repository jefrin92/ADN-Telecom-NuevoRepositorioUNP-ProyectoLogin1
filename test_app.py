import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import current_app

class MyTest(unittest.TestCase):

    def setUp(self):
        from app import app, mysql
        
        self.app = app
        self.mysql = mysql

        self.app.config['TESTING'] = True
        self.app.config['MYSQL_DB'] = 'adn_telecom_test'
        self.client = self.app.test_client()

        self.app_context = self.app.app_context()
        self.app_context.push()

        cur = self.mysql.connection.cursor()
        cur.execute("USE adn_telecom_test")
        cur.close()

    def tearDown(self):
        cur = self.mysql.connection.cursor()
        cur.execute("DELETE FROM componentes")
        cur.execute("DELETE FROM usuarios")
        cur.close()

        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'ADN Telecom', response.data)

    def test_componentes_page(self):
        response = self.client.get('/componentes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Componentes de Red', response.data)

    def test_editar_componente(self):
        cur = self.mysql.connection.cursor()
        cur.execute("""
            INSERT INTO componentes (EQUIPO, MODELO, MARCA, COSTO, descripcion)
            VALUES ('ONU', 'ZXHNF60', 'ZTE', 200.0, 'Descripcion original')
        """)
        self.mysql.connection.commit()
        cur.close()

        response = self.client.post('/editar_componente/1', data=dict(
            equipo='ONU',
            modelo='ZXHNF660',
            marca='ZTE',
            costo='200.0',
            descripcion='Descripción actualizada'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Descripción actualizada'.encode('utf-8'), response.data)

        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM componentes WHERE ID = 1")
        componente = cur.fetchone()
        cur.close()
        self.assertEqual(componente['descripcion'], 'Descripción actualizada')

    def test_delete_component(self):
        cur = self.mysql.connection.cursor()
        cur.execute("""
            INSERT INTO componentes (EQUIPO, MODELO, MARCA, COSTO, descripcion)
            VALUES ('ONU', 'Modelo a eliminar', 'Marca', 200.0, 'Descripción a eliminar')
        """)
        self.mysql.connection.commit()
        cur.close()

        response = self.client.get('/eliminar/1', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b'Modelo a eliminar', response.data)

    def test_register_user(self):
        response = self.client.post('/crear-registro', data=dict(
            txtNombre='Nuevo Usuario',
            txtCorreo='user@example.com',
            txtPassword='123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registro exitoso', response.data)

if __name__ == '__main__':
    unittest.main()