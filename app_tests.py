import os
import app
import unittest

class HomeTestCase(unittest.TestCase):
    def setUp(self):
        app.app.config['TESTING'] = True
        self.app = app.app.test_client()

    def test_home(self):
        rv = self.app.get('/')
        assert 'hello' in rv.data

if __name__ == '__main__':
    unittest.main()
