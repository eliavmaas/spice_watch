import time
import board
import adafruit_dht
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS

# Sensor Setup — DHT22 on GPIO 4
dhtDevice = adafruit_dht.DHT22(board.D4)
location = "pi-zero-1"

# InfluxDB Configuration
url = "http://arrakis.local:8086"  # <-- Replace with your Pi 3 IP
token = "pi_SensorToken2025!"
org = "riderzlabs"
bucket = "arboretum"

client = InfluxDBClient(url=url, token=token, org=org, timeout=10_000)
write_api = client.write_api(write_options=SYNCHRONOUS)

while True:
    try:
        temp_c = dhtDevice.temperature
        humidity = dhtDevice.humidity

        if temp_c is None or humidity is None:
            raise RuntimeError("Sensor returned None")

        print(f"Temp={temp_c:.1f}C Humidity={humidity:.1f}%")

        point = (
            Point("environment")
            .tag("location", location)
            .field("temperature", float(temp_c))
            .field("humidity", float(humidity))
        )

        write_api.write(bucket=bucket, org=org, record=point)

    except RuntimeError as e:
        print(f"DHT22 sensor error: {e}")
        time.sleep(2)  # Retry sooner for sensor glitches
        continue
    except Exception as e:
        print(f"Unexpected error: {e}")
        time.sleep(10)  # Slow down on Influx or system errors
        continue

    time.sleep(5)