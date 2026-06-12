"""
Skenario 1: Komunikasi Dasar Publisher–Subscriber
Studi Kasus: Smart Room Monitoring
Publisher: Mengirim data sensor suhu dan kelembaban ruangan
"""

import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime

# Konfigurasi Broker
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "smartroom/sensor/basic"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[Publisher] Terhubung ke Mosquitto Broker: {BROKER_HOST}:{BROKER_PORT}")
    else:
        print(f"[Publisher] Gagal terhubung. Kode: {rc}")

def on_publish(client, userdata, mid):
    print(f"[Publisher] Pesan berhasil dikirim (MID: {mid})")

def create_sensor_data():
    """Simulasi data sensor suhu & kelembaban ruangan"""
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "room": "Ruang Tamu",
        "temperature_c": round(random.uniform(24.0, 32.0), 2),
        "humidity_pct": round(random.uniform(50.0, 80.0), 2),
        "status": "normal"
    }

def main():
    client = mqtt.Client(client_id="publisher_scenario1")
    client.on_connect = on_connect
    client.on_publish = on_publish

    print("=" * 55)
    print("  Skenario 1: Komunikasi Dasar Publisher-Subscriber")
    print("  Smart Room Monitoring - Suhu & Kelembaban")
    print("=" * 55)

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()

    try:
        for i in range(5):
            data = create_sensor_data()
            payload = json.dumps(data)
            result = client.publish(TOPIC, payload, qos=0)
            print(f"\n[Publisher] Mengirim pesan ke-{i+1}:")
            print(f"  Topik   : {TOPIC}")
            print(f"  Payload : {payload}")
            time.sleep(2)
    except KeyboardInterrupt:
        print("\n[Publisher] Dihentikan oleh pengguna.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[Publisher] Koneksi ditutup.")

if __name__ == "__main__":
    main()
