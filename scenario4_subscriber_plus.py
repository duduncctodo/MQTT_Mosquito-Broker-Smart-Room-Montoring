"""
Skenario 4: Penggunaan Wildcard '+'
Studi Kasus: Smart Room Monitoring
Subscriber: Menggunakan wildcard '+' (satu level) untuk subscribe topik

Wildcard '+' menggantikan TEPAT SATU level topik.
Contoh: smartroom/+/temperature  → menangkap semua sensor suhu di semua ruangan
         smartroom/ruang_tamu/+ → menangkap semua sensor di ruang tamu
"""

import paho.mqtt.client as mqtt
import json
from datetime import datetime
from collections import defaultdict

BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Wildcard '+' — hanya satu level
WILDCARD_SUBSCRIPTIONS = [
    ("smartroom/+/temperature", 1),   # Semua sensor suhu, semua ruangan
    ("smartroom/+/motion",      1),   # Semua sensor gerak, semua ruangan
    ("smartroom/ruang_tamu/+",  1),   # Semua sensor di ruang tamu
]

stats = defaultdict(int)

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[Subscriber '+'] Terhubung ke Broker: {BROKER_HOST}:{BROKER_PORT}")
        for topic, qos in WILDCARD_SUBSCRIPTIONS:
            client.subscribe(topic, qos=qos)
        print("\n[Subscriber '+'] Subscribe dengan wildcard '+':")
        for topic, qos in WILDCARD_SUBSCRIPTIONS:
            print(f"  Pattern: {topic}  (QoS {qos})")
        print("\nCatatan: '+' hanya menangkap SATU level topik\n")

def on_message(client, userdata, msg):
    recv_time = datetime.now().strftime("%H:%M:%S")
    try:
        data = json.loads(msg.payload.decode())
        stats[msg.topic] += 1
        parts = msg.topic.split("/")
        room  = parts[1] if len(parts) > 1 else "-"
        sensor= parts[2] if len(parts) > 2 else "-"

        print(f"[{recv_time}] Topik aktual: {msg.topic}")
        print(f"  Ruangan: {room}  |  Sensor: {sensor}  |  Nilai: {data.get('value','-')}")
        # Topik dengan lebih dari 3 level TIDAK akan ditangkap '+' (hanya '#' yang bisa)
        if len(parts) > 3:
            print(f"  ⚠ Ini topik dalam (level {len(parts)}) — seharusnya tidak muncul dengan '+'!")

    except Exception as e:
        print(f"[Subscriber] Error: {e}")

def main():
    client = mqtt.Client(client_id="subscriber_plus_wildcard_sc4")
    client.on_connect = on_connect
    client.on_message = on_message

    print("=" * 65)
    print("  Skenario 4: Wildcard '+' (Single-Level)")
    print("  Smart Room Monitoring - Subscriber")
    print("=" * 65)
    print("[Subscriber] Menunggu pesan... (Ctrl+C untuk berhenti)\n")

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("\n\n[Subscriber '+'] Statistik Topik yang Ditangkap:")
        print(f"  {'Topik Aktual':<50} {'Jumlah':>6}")
        print("  " + "-"*58)
        for topic, count in sorted(stats.items()):
            print(f"  {topic:<50} {count:>6}")
        total = sum(stats.values())
        print(f"\n  Total pesan ditangkap wildcard '+': {total}")
        print("  (Topik lebih dari 3 level TIDAK tertangkap oleh '+')")
        client.disconnect()

if __name__ == "__main__":
    main()
