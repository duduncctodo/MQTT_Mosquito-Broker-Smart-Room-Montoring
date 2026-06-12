"""
Skenario 5: Penggunaan Wildcard '#'
Studi Kasus: Smart Room Monitoring
Subscriber: Menggunakan wildcard '#' (multi-level) untuk subscribe topik

Wildcard '#' menggantikan SEMUA level topik di bawahnya (termasuk subtopik dalam).
Contoh: smartroom/#           → semua topik di bawah smartroom
         smartroom/dapur/#   → semua topik di bawah smartroom/dapur
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime
from collections import defaultdict

BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Wildcard '#' — semua level di bawah prefix
WILDCARD_SUBSCRIPTIONS = [
    ("smartroom/#",              1),   # SEMUA topik di dalam smartroom
    ("smartroom/dapur/#",        1),   # Semua topik di bawah dapur
    ("smartroom/kamar_tidur/#",  1),   # Semua topik di bawah kamar_tidur
]

stats       = defaultdict(int)
depth_stats = defaultdict(int)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[Subscriber '#'] Terhubung ke Broker: {BROKER_HOST}:{BROKER_PORT}")
        for topic, qos in WILDCARD_SUBSCRIPTIONS:
            client.subscribe(topic, qos=qos)
        print("\n[Subscriber '#'] Subscribe dengan wildcard '#':")
        for topic, qos in WILDCARD_SUBSCRIPTIONS:
            print(f"  Pattern: {topic}  (QoS {qos})")
        print("\nCatatan: '#' menangkap SEMUA level topik di bawahnya\n")

def on_message(client, userdata, msg):
    recv_time = datetime.now().strftime("%H:%M:%S")
    try:
        data  = json.loads(msg.payload.decode())
        parts = msg.topic.split("/")
        depth = len(parts)
        stats[msg.topic] += 1
        depth_stats[depth] += 1

        depth_label = f"[Level-{depth}]"
        print(f"[{recv_time}] {depth_label} Topik: {msg.topic}")
        print(f"  Sensor: {data.get('sensor','-')}  |  Nilai: {data.get('value','-')}")
        if depth > 3:
            print(f"  ✔ Topik DALAM (level {depth}) tertangkap '#' (tidak bisa ditangkap '+')")
    except Exception as e:
        print(f"[Subscriber] Error: {e}")

def main():
    client = mqtt.Client(client_id="subscriber_hash_wildcard_sc5")
    client.on_connect = on_connect
    client.on_message = on_message

    print("=" * 65)
    print("  Skenario 5: Wildcard '#' (Multi-Level)")
    print("  Smart Room Monitoring - Subscriber")
    print("=" * 65)
    print("[Subscriber] Menunggu pesan... (Ctrl+C untuk berhenti)\n")

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n\n[Subscriber '#'] Statistik Akhir:")
        print(f"\n  Distribusi berdasarkan kedalaman topik:")
        for depth, count in sorted(depth_stats.items()):
            bar = "█" * count
            print(f"    Level-{depth}: {count:>3} pesan  {bar}")

        print(f"\n  Total topik unik tertangkap : {len(stats)}")
        print(f"  Total pesan diterima '#'    : {sum(stats.values())}")
        print("\n  Perbandingan: wildcard '+' hanya menangkap topik level-3,")
        print("  sedangkan '#' menangkap level-3 DAN level-4 (subtopik dalam).")
        client.disconnect()

if __name__ == "__main__":
    main()
