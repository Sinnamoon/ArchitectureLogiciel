import os
from dotenv import load_dotenv
import time
import requests
from influxdb_client_3 import Point, InfluxDBClient3, flight_client_options
import certifi

os.environ['GRPC_DEFAULT_SSL_ROOTS_FILE_PATH'] = certifi.where()

load_dotenv()  # take environment variables from .env.

# Configuration
fh = open(certifi.where(), "r")
cert = fh.read()
fh.close()

api_url = 'http://10.31.33.62:3001/cars'  # Replace with your API URL
app_id = '60e3f3d8b5e9c6a5d8f4b0c5'  # Your app-id
influxdb_url = 'https://eu-central-1-1.aws.cloud2.influxdata.com/'
token = os.getenv("INFLUXDB_TOKEN")
org = 'Dashboard'  # Replace with your InfluxDB organization name
bucket = 'Cars'  # Replace with your InfluxDB bucket name
database = "Cars"


# Fetch data from API
response = requests.get(api_url, headers={'App-id': app_id})
data = response.json()  # Parse JSON string into Python object

if isinstance(data, dict):
    data = [data]

# Initialize InfluxDB client
client = InfluxDBClient3(host='https://eu-central-1-1.aws.cloud2.influxdata.com', token=token, org=org, fco=flight_client_options(tls_root_certs=cert))

# Prepare data for InfluxDB
for item in data:
    point = Point("Car")  # Measurement name is "Car"
    point.tag("brand", item["brand"])  # Tag for brand
    point.tag("model", item["model"])  # Tag for model
    point.tag("plate", item["plate"])  # Tag for plate
    point.field("year", item["year"])  # Field for year
    point.field("lat", item["lat"])  # Field for latitude
    point.field("lon", item["lon"])  # Field for longitude
    point.field("speed", item["speed"])  # Field for speed
    point.field("acceleration", item["acceleration"])  # Field for acceleration
    point.field("created_at_pour_les_relous", item["created_at_pour_les_relous"])
    point.field("updated_at_pour_les_relous", item["updated_at_pour_les_relous"])
    client.write(database=database, record=point)
    time.sleep(1)  # separate points by 1 second

    print(f"data written to InfluxDB")

# Close the client
client.close()
