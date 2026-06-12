"""
Skenario 1: Komunikasi Dasar Publisher–Subscriber
Studi Kasus: Smart Room Monitoring
Subscriber: Menerima data sensor suhu dan kelembaban ruangan
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Konfigurasi Broker
BROKER_HOST = "localhost"
BROKER_PORT = 1883
TOPIC = "smartroom/sensor/basic"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[Subscriber] Terhubung ke Broker: {BROKER_HOST}:{BROKER_PORT}")
        client.subscribe(TOPIC, qos=0)
        print(f"[Subscriber] Subscribe ke topik: {TOPIC}")
    else:
        print(f"[Subscriber] Gagal terhubung. Kode: {rc}")

def on_message(client, userdata, msg):
    receive_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        data = json.loads(msg.payload.decode())
        print(f"\n[Subscriber] Pesan diterima pukul {receive_time}:")
        print(f"  Topik       : {msg.topic}")
        print(f"  QoS         : {msg.qos}")
        print(f"  Ruangan     : {data.get('room', '-')}")
        print(f"  Suhu        : {data.get('temperature_c', '-')} °C")
        print(f"  Kelembaban  : {data.get('humidity_pct', '-')} %")
        print(f"  Status      : {data.get('status', '-')}")
        print(f"  Timestamp   : {data.get('timestamp', '-')}")
    except Exception as e:
        print(f"[Subscriber] Error parsing pesan: {e}")
        print(f"  Raw payload : {msg.payload.decode()}")

def on_subscribe(client, userdata, mid, granted_qos):
    print(f"[Subscriber] Subscribe berhasil. QoS diberikan: {granted_qos}")

def main():
    client = mqtt.Client(client_id="subscriber_scenario1")
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_subscribe = on_subscribe

    print("=" * 55)
    print("  Skenario 1: Komunikasi Dasar Publisher-Subscriber")
    print("  Smart Room Monitoring - Subscriber")
    print("=" * 55)
    print("[Subscriber] Menunggu pesan... (Ctrl+C untuk berhenti)\n")

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)

    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n[Subscriber] Dihentikan oleh pengguna.")
    finally:
        client.disconnect()
        print("[Subscriber] Koneksi ditutup.")

if __name__ == "__main__":
    main()
