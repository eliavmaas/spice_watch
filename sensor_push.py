import time
import board
import adafruit_dht
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# DHT11 setup
dhtDevice = adafruit_dht.DHT11(board.D4)

# InfluxDB config
url = "http://localhost:8086"
token = "pi_SensorToken2025!"
org = "riderzlabs"
bucket = "arboretum"
location = "pi3-sensor"

client = InfluxDBClient(url=url, token=token, org=org)
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
        print(f"Runtime Error: {e}")
        time.sleep(2)
        continue
    except Exception as e:
        print(f"Unexpected Error: {e}")
        break

    time.sleep(10)
