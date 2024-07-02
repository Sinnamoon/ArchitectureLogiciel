import os
import certifi
from dotenv import load_dotenv
from influxdb_client_3 import Point, InfluxDBClient3, flight_client_options

os.environ['GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'] = certifi.where()

load_dotenv()  # take environment variables from .env.

influxdb_url = 'https://eu-central-1-1.aws.cloud2.influxdata.com/'
token = os.getenv("INFLUXDB_TOKEN")
org = 'Dashboard'  # Replace with your InfluxDB organization name
bucket = 'Cars'  # Replace with your InfluxDB bucket name
database = "Cars"

# Configuration
fh = open(certifi.where(), "r")
cert = fh.read()
fh.close()

client = InfluxDBClient3(host='https://eu-central-1-1.aws.cloud2.influxdata.com', token=token, org=org, fco=flight_client_options(tls_root_certs=cert))

table = client.query('select * from "Car"', database=database, mode='pandas', language="sql")

print(table)
