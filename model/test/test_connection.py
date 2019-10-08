import unittest
from influxdb import InfluxDBClient


class TestConnection(unittest.TestCase):

    def test_conntection_to_influx_db(self):
        client = InfluxDBClient('influxdb.weberandreas.eu',
                                ssl=True,
                                port=443,
                                username='admin',
                                password='css-secret-password',
                                database='css')
        client.ping()
