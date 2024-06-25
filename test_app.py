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
        cur.execute("DELETE FROM componentes")  # Limpiar la tabla componentes
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
            INSERT INTO componentes (EQUIPO, MODELO, MARCA, COSTO, Velocidad_Red, Year, Estructura_Red, Nro_Puertos, descripcion, Imagen)
            VALUES ('ONU', 'ZXHNF60', 'ZTE', 200.0, '1000', 2022, 'Gigabit', 24, 'Descripcion original', 'https://example.com/image.jpg')
        """)
        self.mysql.connection.commit()
        inserted_id = cur.lastrowid
        cur.close()

        response = self.client.post(f'/editar_componente/{inserted_id}', data=dict(
            EQUIPO='ONU',
            MODELO='ZXHNF660',
            MARCA='ZTE',
            COSTO='200.0',
            Velocidad_Red='1000',
            Year='2022',
            Estructura_Red='Gigabit',
            Nro_Puertos='24',
            descripcion='Descripción actualizada',
            Imagen='https://example.com/image.jpg'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM componentes WHERE ID = %s", (inserted_id,))
        componente = cur.fetchone()
        cur.close()

        print("Componente encontrado:", componente)  # Agregar esto para depuración

        self.assertIsNotNone(componente)
        self.assertEqual(componente['descripcion'], 'Descripción actualizada')

    def test_agregar_componente(self):
        unique_model = 'UNIQUE_MODEL_123'  # Asegúrate de que este modelo es único
        response = self.client.post('/agregar_componente', data=dict(
            EQUIPO='ONU',
            MODELO=unique_model,
            MARCA='ZTE',
            COSTO='200.0',
            Velocidad_Red='1000',
            Year='2022',
            Estructura_Red='Gigabit',
            Nro_Puertos='24',
            descripcion='Nuevo componente',
            Imagen='https://example.com/image.jpg'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Nuevo componente'.encode('utf-8'), response.data)

        cur = self.mysql.connection.cursor()
        cur.execute("SELECT * FROM componentes WHERE MODELO = %s", (unique_model,))
        componente = cur.fetchone()
        cur.close()
        self.assertIsNotNone(componente)
        self.assertEqual(componente['descripcion'], 'Nuevo componente')

    def test_register_user(self):
        response = self.client.post('/crear-registro', data=dict(
            txtNombre='Nuevo Usuario',
            txtCorreo='ulises@example.com',
            txtPassword='123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Registro exitoso', response.data)

if __name__ == '__main__':
    unittest.main()