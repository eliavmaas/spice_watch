import time
import board
import adafruit_dht
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Sensor Setup
dhtDevice = adafruit_dht.DHT11(board.D4)
location = "pi3-sensor"

# InfluxDB Configuration
url = "http://localhost:8086"
token = "!"
org = ""
bucket = ""

# Connect to InfluxDB
client = InfluxDBClient(url=url, token=token, org=org, timeout=10_000)
write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    try:
        temp_c = float(dhtDevice.temperature)
        humidity = float(dhtDevice.humidity)

        print(f"Temp={temp_c:.1f}C Humidity={humidity:.1f}%")

        point = (
            Point("environment")
            .tag("location", location)
            .field("temperature", temp_c)
            .field("humidity", humidity)
        )

        write_api.write(bucket=bucket, org=org, record=point)

    except RuntimeError as e:
        print(f"DHT11 sensor error: {e}")
        # DHT11 can fail intermittently — we keep going
    except Exception as e:
        print(f"Unexpected error: {e}")
        # Optional: sleep longer if Influx fails
        time.sleep(5)

    time.sleep(5)  # Wait before next reading
