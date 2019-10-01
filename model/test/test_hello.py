import unittest
from hello import say_hello
from influxdb import InfluxDBClient


class TestHello(unittest.TestCase):

    def test_say_hello(self):
        self.assertEqual(say_hello('VS Code'), 'Hello VS Code')

    def test_conntection_to_influx_db(self):
        client = InfluxDBClient('influxdb.weberandreas.eu',
                                ssl=True,
                                port=443,
                                username='admin',
                                password='css-secret-password',
                                database='css')
        client.ping()
