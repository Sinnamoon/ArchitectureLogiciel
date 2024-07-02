import socketio
import os
from dotenv import load_dotenv
from influxdb_client_3 import Point, InfluxDBClient3, flight_client_options
import certifi

load_dotenv()  # take environment variables from .env.

# Configuration
fh = open(certifi.where(), "r")
cert = fh.read()
fh.close()

token = os.getenv("INFLUXDB_TOKEN")
appId = os.getenv("APP_ID")
org = 'Dashboard'  # Replace with your InfluxDB organization name
database = "Cars"

# Initialize InfluxDB client
client = InfluxDBClient3(host='https://eu-central-1-1.aws.cloud2.influxdata.com', token=token, org=org,
                         fco=flight_client_options(tls_root_certs=cert))

sio = socketio.Client()


@sio.event
def connect():
    print('connection established')


@sio.event
def disconnect():
    print('disconnected from server')


@sio.event
def carPosition(data):  # Add 'data' as an argument
    print('Car position received:', data)  # Print the received data

    if not data:
        print("Received empty data.")
        return "No data received"

    car_data = data.get('message', {})

    # Prepare data for InfluxDB
    point = Point("Car")  # Measurement name is "Car"
    for key, value in car_data.items():  # Change to car_data.items()
        if isinstance(value, (int, float)):
            point.field(key, value)  # Field for each numeric item in data
        else:
            point.tag(key, value)  # Tag for each non-numeric item in data

    # Debugging: Print the Point object
    print("Point to write to InfluxDB:", point)

    try:
        client.write(database=database, record=point)
        print(f"Data written to InfluxDB")
    except Exception as e:
        print(f"Error writing to InfluxDB: {e}")

    return "OK"


sio.connect('ws://10.31.33.62:3001', headers={'App-id': appId})
sio.wait()
