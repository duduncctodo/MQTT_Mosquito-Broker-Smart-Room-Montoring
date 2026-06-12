"""
Skenario 4 & 5: Wildcard Topic '+' dan '#'
Studi Kasus: Smart Room Monitoring
Publisher: Mengirim ke berbagai subtopik untuk uji wildcard
"""

import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime

BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Semua topik yang akan dipublish (untuk menguji wildcard)
ALL_TOPICS = [
    "smartroom/ruang_tamu/temperature",
    "smartroom/ruang_tamu/humidity",
    "smartroom/ruang_tamu/motion",
    "smartroom/kamar_tidur/temperature",
    "smartroom/kamar_tidur/light",
    "smartroom/dapur/co2",
    "smartroom/dapur/temperature",
    "smartroom/garasi/motion",
    "smartroom/garasi/door",
    # Topik lebih dalam (hanya ditangkap '#')
    "smartroom/ruang_tamu/temperature/detail",
    "smartroom/kamar_tidur/light/brightness",
]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[Publisher Wildcard] Terhubung ke Broker: {BROKER_HOST}:{BROKER_PORT}")

def generate_data(topic):
    parts = topic.split("/")
    sensor = parts[2] if len(parts) > 2 else "unknown"
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "topic": topic,
        "sensor": sensor,
        "value": round(random.uniform(10, 100), 2),
        "unit": "varies",
        "message": f"Data dari {topic}"
    }

def main():
    client = mqtt.Client(client_id="publisher_wildcard_sc45")
    client.on_connect = on_connect

    print("=" * 65)
    print("  Skenario 4 & 5: Publisher untuk Uji Wildcard '+' dan '#'")
    print("  Smart Room Monitoring")
    print("=" * 65)

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()
    time.sleep(0.5)

    try:
        for round_num in range(3):
            print(f"\n{'─'*65}")
            print(f"  Putaran {round_num+1}: Mempublish ke {len(ALL_TOPICS)} topik")
            print(f"{'─'*65}")
            for topic in ALL_TOPICS:
                data    = generate_data(topic)
                payload = json.dumps(data)
                client.publish(topic, payload, qos=1)
                depth = topic.count("/")
                print(f"  [{depth} level] {topic}")
                time.sleep(0.3)
            time.sleep(3)

    except KeyboardInterrupt:
        print("\n[Publisher] Dihentikan.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[Publisher] Koneksi ditutup.")

if __name__ == "__main__":
    main()
