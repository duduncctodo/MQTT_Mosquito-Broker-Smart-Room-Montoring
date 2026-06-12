"""
Skenario 3: Penggunaan Beberapa Topik
Studi Kasus: Smart Room Monitoring
Subscriber: Subscribe ke beberapa topik eksplisit sekaligus
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime
from collections import defaultdict

BROKER_HOST = "localhost"
BROKER_PORT = 1883

SUBSCRIPTIONS = [
    ("smartroom/ruang_tamu/temperature", 1),
    ("smartroom/ruang_tamu/humidity",    1),
    ("smartroom/ruang_tamu/motion",      1),
    ("smartroom/kamar_tidur/temperature",1),
    ("smartroom/kamar_tidur/light",      1),
    ("smartroom/dapur/co2",              1),
]

stats = defaultdict(int)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[Subscriber] Terhubung ke Broker: {BROKER_HOST}:{BROKER_PORT}")
        for topic, qos in SUBSCRIPTIONS:
            client.subscribe(topic, qos=qos)
        print(f"[Subscriber] Subscribe ke {len(SUBSCRIPTIONS)} topik:")
        for topic, qos in SUBSCRIPTIONS:
            print(f"  - {topic}  (QoS {qos})")

def on_message(client, userdata, msg):
    recv_time = datetime.now().strftime("%H:%M:%S")
    try:
        data = json.loads(msg.payload.decode())
        stats[msg.topic] += 1

        print(f"\n[{recv_time}] Pesan #{stats[msg.topic]} dari topik: {msg.topic}")
        print(f"  Ruangan  : {data.get('room', '-')}")
        print(f"  Sensor   : {data.get('sensor', '-').upper()}")
        print(f"  Nilai    : {data.get('value', '-')} {data.get('unit', '')}")
        print(f"  Status   : {data.get('status', '-')}")
    except Exception as e:
        print(f"[Subscriber] Error parsing: {e}")

def main():
    client = mqtt.Client(client_id="subscriber_multitopic_scenario3")
    client.on_connect = on_connect
    client.on_message = on_message

    print("=" * 60)
    print("  Skenario 3: Subscriber Multi-Topik")
    print("  Smart Room Monitoring")
    print("=" * 60)
    print("[Subscriber] Menunggu pesan... (Ctrl+C untuk berhenti)\n")

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n\n[Subscriber] Statistik Pesan per Topik:")
        print(f"{'Topik':<45} {'Jumlah':>6}")
        print("-" * 53)
        for topic, count in sorted(stats.items()):
            print(f"  {topic:<43} {count:>6}")
        print(f"\n  Total pesan diterima: {sum(stats.values())}")
        client.disconnect()

if __name__ == "__main__":
    main()
