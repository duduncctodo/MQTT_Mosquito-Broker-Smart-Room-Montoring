"""
Skenario 2: Pengiriman Data dengan QoS Berbeda (QoS 0, 1, 2)
Studi Kasus: Smart Room Monitoring
Subscriber: Menerima pesan dari semua level QoS
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime

BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Subscribe ke semua topik QoS
SUBSCRIPTIONS = [
    ("smartroom/qos/level0", 0),
    ("smartroom/qos/level1", 1),
    ("smartroom/qos/level2", 2),
]

message_count = {0: 0, 1: 0, 2: 0}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[Subscriber QoS] Terhubung ke Broker: {BROKER_HOST}:{BROKER_PORT}")
        for topic, qos in SUBSCRIPTIONS:
            client.subscribe(topic, qos=qos)
            print(f"  Subscribe: {topic}  (QoS {qos})")
    else:
        print(f"[Subscriber QoS] Gagal terhubung. Kode: {rc}")

def on_message(client, userdata, msg):
    recv_time = datetime.now().strftime("%H:%M:%S")
    try:
        data = json.loads(msg.payload.decode())
        qos  = msg.qos
        message_count[qos] = message_count.get(qos, 0) + 1

        print(f"\n[{recv_time}] Pesan diterima (QoS {qos}):")
        print(f"  Topik    : {msg.topic}")
        print(f"  Ruangan  : {data.get('room', '-')}")
        print(f"  Suhu     : {data.get('temperature_c', '-')} °C")
        print(f"  Alert    : {data.get('alert', '-')}")
        print(f"  Total QoS {qos}: {message_count[qos]} pesan diterima")
    except Exception as e:
        print(f"[Subscriber] Error: {e}")

def main():
    client = mqtt.Client(client_id="subscriber_qos_scenario2")
    client.on_connect = on_connect
    client.on_message = on_message

    print("=" * 60)
    print("  Skenario 2: Subscriber Multi-QoS")
    print("  Smart Room Monitoring")
    print("=" * 60)
    print("[Subscriber] Menunggu pesan... (Ctrl+C untuk berhenti)\n")

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n\n[Subscriber] Statistik Akhir:")
        for qos, count in message_count.items():
            print(f"  QoS {qos}: {count} pesan diterima")
        client.disconnect()

if __name__ == "__main__":
    main()
