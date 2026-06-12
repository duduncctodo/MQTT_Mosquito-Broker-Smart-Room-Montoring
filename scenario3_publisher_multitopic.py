"""
Skenario 3: Penggunaan Beberapa Topik
Studi Kasus: Smart Room Monitoring
Publisher: Mengirim data ke beberapa topik berbeda (sensor berbeda, ruangan berbeda)
"""

import paho.mqtt.client as mqtt
import time
import json
import random
from datetime import datetime

BROKER_HOST = "localhost"
BROKER_PORT = 1883

# Struktur topik hierarkis: smartroom/<ruangan>/<sensor>
TOPICS = {
    "suhu_ruang_tamu"    : "smartroom/ruang_tamu/temperature",
    "kelembaban_ruang"   : "smartroom/ruang_tamu/humidity",
    "gerak_ruang"        : "smartroom/ruang_tamu/motion",
    "suhu_kamar"         : "smartroom/kamar_tidur/temperature",
    "cahaya_kamar"       : "smartroom/kamar_tidur/light",
    "co2_dapur"          : "smartroom/dapur/co2",
}

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"[Publisher] Terhubung ke Broker: {BROKER_HOST}:{BROKER_PORT}")

def on_publish(client, userdata, mid):
    pass  # Suppress per-message output for cleaner multi-topic demo

def generate_sensor_data(sensor_type, room):
    base = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "room": room,
        "sensor": sensor_type,
    }
    if sensor_type == "temperature":
        base["value"] = round(random.uniform(22.0, 36.0), 2)
        base["unit"] = "°C"
        base["status"] = "HIGH" if base["value"] > 32 else "NORMAL"
    elif sensor_type == "humidity":
        base["value"] = round(random.uniform(40.0, 90.0), 2)
        base["unit"] = "%"
        base["status"] = "HIGH" if base["value"] > 75 else "NORMAL"
    elif sensor_type == "motion":
        base["value"] = random.choice([True, False])
        base["unit"] = "boolean"
        base["status"] = "DETECTED" if base["value"] else "CLEAR"
    elif sensor_type == "light":
        base["value"] = random.randint(100, 800)
        base["unit"] = "lux"
        base["status"] = "DIM" if base["value"] < 300 else "BRIGHT"
    elif sensor_type == "co2":
        base["value"] = random.randint(400, 1200)
        base["unit"] = "ppm"
        base["status"] = "DANGER" if base["value"] > 1000 else "SAFE"
    return base

def main():
    client = mqtt.Client(client_id="publisher_multitopic_scenario3")
    client.on_connect = on_connect
    client.on_publish = on_publish

    print("=" * 60)
    print("  Skenario 3: Publisher Multi-Topik")
    print("  Smart Room Monitoring - Berbagai Sensor & Ruangan")
    print("=" * 60)

    client.connect(BROKER_HOST, BROKER_PORT, keepalive=60)
    client.loop_start()
    time.sleep(0.5)

    topic_map = {
        "suhu_ruang_tamu" : ("temperature", "Ruang Tamu"),
        "kelembaban_ruang": ("humidity",    "Ruang Tamu"),
        "gerak_ruang"     : ("motion",      "Ruang Tamu"),
        "suhu_kamar"      : ("temperature", "Kamar Tidur"),
        "cahaya_kamar"    : ("light",       "Kamar Tidur"),
        "co2_dapur"       : ("co2",         "Dapur"),
    }

    try:
        for round_num in range(3):
            print(f"\n{'═'*60}")
            print(f"  Putaran ke-{round_num + 1}")
            print(f"{'═'*60}")
            for key, (sensor_type, room) in topic_map.items():
                topic   = TOPICS[key]
                data    = generate_sensor_data(sensor_type, room)
                payload = json.dumps(data)
                client.publish(topic, payload, qos=1)
                print(f"\n  Topik   : {topic}")
                print(f"  Sensor  : {sensor_type.upper()} | Ruangan: {room}")
                print(f"  Nilai   : {data['value']} {data['unit']} | Status: {data['status']}")
                time.sleep(0.5)
            time.sleep(2)

    except KeyboardInterrupt:
        print("\n[Publisher] Dihentikan.")
    finally:
        client.loop_stop()
        client.disconnect()
        print("[Publisher] Koneksi ditutup.")

if __name__ == "__main__":
    main()
