"""
Skenario 2: Pengiriman Data dengan QoS Berbeda (QoS 0, 1, 2)
Studi Kasus: Smart Room Monitoring
Publisher: Mengirim data dengan variasi QoS 0, 1, dan 2
"""

import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime

BROKER_HOST = "localhost"
BROKER_PORT = 1883

QOS_TOPICS = {
    0: "smartroom/qos/level0",
    1: "smartroom/qos/level1",
    2: "smartroom/qos/level2",
}

QOS_DESCRIPTIONS = {
    0: "At most once  - Fire and Forget (tidak ada konfirmasi)",
    1: "At least once - Pesan dijamin sampai minimal 1 kali",
    2: "Exactly once  - Pesan dijamin tepat 1 kali (paling aman)",
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[Publisher QoS] Terhubung ke Broker: {BROKER_HOST}:{BROKER_PORT}")
    else:
        print(f"[Publisher QoS] Gagal terhubung. Kode: {rc}")

def on_publish(client, userdata, mid):
    print(f"  >> Konfirmasi pengiriman (MID: {mid}) diterima dari broker.")

def create_room_alert(room, qos_level):
    """Simulasi data peringatan kondisi ruangan"""
    temp = round(random.uniform(28.0, 38.0), 2)
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "room": room,
        "temperature_c": temp,
        "alert": "HIGH TEMP" if temp > 33 else "NORMAL",
        "qos_level": qos_level,
        "message": f"Data dikirim dengan QoS {qos_level}"
    }

def main():
    client = mqtt.Client(client_id="publisher_qos_scenario2")
    client.on_connect = on_connect
    client.on_publish = on_publish

    print("=" * 60)
    print("  Skenario 2: Pengiriman Data dengan Variasi QoS")
    print("  Smart Room Monitoring - QoS 0, 1, 2")
    print("=" * 60)

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()
    time.sleep(1)

    rooms = ["Ruang Tamu", "Kamar Tidur", "Dapur"]

    try:
        for qos_level in [0, 1, 2]:
            topic = QOS_TOPICS[qos_level]
            desc  = QOS_DESCRIPTIONS[qos_level]
            room  = rooms[qos_level]

            print(f"\n{'─'*60}")
            print(f"[Publisher] Mengirim dengan QoS {qos_level}")
            print(f"  Deskripsi : {desc}")
            print(f"  Topik     : {topic}")

            for i in range(3):
                data    = create_room_alert(room, qos_level)
                payload = json.dumps(data)
                result  = client.publish(topic, payload, qos=qos_level)
                print(f"\n  [Pesan {i+1}] Dikirim:")
                print(f"    Suhu    : {data['temperature_c']} °C  |  Alert: {data['alert']}")
                print(f"    Payload : {payload[:80]}...")
                time.sleep(1.5)

            time.sleep(1)

    except KeyboardInterrupt:
        print("\n[Publisher] Dihentikan.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("\n[Publisher] Koneksi ditutup.")

if __name__ == "__main__":
    main()
