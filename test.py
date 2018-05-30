import unittest, os
from app import create_app
from app.db import db

app = create_app('test')

class TestCase(unittest.TestCase):

    def setup(self):
        db.init_app(app)

    def tearDown(self):
        os.remove(app.config.get('SQLALCHEMY_DATABASE_URI')[10:])

    def test_create_user(self):
        with app.test_client() as client:
            response = client.post('/register', data=dict(
                    username='rino',
                    password='1234'
                ))
            print(response)
            assert 'User created successfully.' in str(response.data)


if __name__ == '__main__':
    unittest.main()
