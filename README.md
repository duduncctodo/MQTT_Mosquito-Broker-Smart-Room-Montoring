# Smart Room Monitoring — Sistem Komunikasi MQTT

Sistem komunikasi berbasis MQTT untuk simulasi pemantauan ruangan cerdas. Dibangun menggunakan Mosquitto sebagai message broker dan `paho-mqtt` sebagai library client Python. Proyek ini mendemonstrasikan pola komunikasi publish-subscribe melalui lima skenario yang mencakup komunikasi dasar, variasi QoS, multi-topik, dan wildcard subscription.

Dibuat sebagai tugas praktikum mata kuliah Cyber Physical System.

---

## Deskripsi Sistem

Sistem mensimulasikan data sensor dari beberapa ruangan (ruang tamu, kamar tidur, dapur, garasi). Setiap ruangan mempublish pembacaan sensor ke hierarki topik yang terstruktur. Subscriber memfilter pesan menggunakan topik eksplisit maupun wildcard MQTT.

**Skenario yang diimplementasikan:**

| No | Skenario | Deskripsi |
|----|----------|-----------|
| 1 | Komunikasi dasar | Publisher mengirim data suhu dan kelembaban, subscriber menerima dan menampilkan |
| 2 | Variasi QoS | Data yang sama dikirim dengan QoS 0, 1, dan 2 untuk membandingkan jaminan pengiriman |
| 3 | Multi-topik | Enam jenis sensor di tiga ruangan, masing-masing pada topik tersendiri |
| 4 | Wildcard `+` | Wildcard satu level yang mencocokkan satu segmen dalam path topik |
| 5 | Wildcard `#` | Wildcard multi-level yang menangkap semua subtopik di bawah suatu prefix |

---

## Kebutuhan Sistem

- Python 3.7 ke atas
- Mosquitto MQTT Broker
- Visual Studio Code
- Library paho-mqtt

---

## Instalasi

### 1. Install Visual Studio Code

Download dan install VS Code dari [https://code.visualstudio.com](https://code.visualstudio.com).

Setelah terpasang, buka VS Code lalu install extension **Python** dari Microsoft melalui menu Extensions (`Ctrl+Shift+X`).

### 2. Install Mosquitto Broker

Download installer dari [https://mosquitto.org/download](https://mosquitto.org/download), pilih versi **Windows (64-bit)**.

Jalankan installer sebagai Administrator dan pastikan opsi **Install as Windows Service** dicentang.

Setelah terinstall, temukan file konfigurasi Mosquitto (biasanya di `C:\Program Files\mosquitto\mosquitto.conf` atau `C:\mosquitto\mosquitto.conf`) lalu tambahkan baris berikut di bagian paling bawah:

```
listener 1883 localhost
allow_anonymous true
```

Simpan file, kemudian restart service Mosquitto melalui `services.msc` (tekan `Win+R`, ketik `services.msc`, cari **Mosquitto Broker**, klik kanan, pilih **Restart**).

Untuk memverifikasi broker berjalan, buka Command Prompt dan ketik:

```
mosquitto_sub -h localhost -p 1883 -t "test" -v
```

Jika tidak ada error, broker sudah aktif.

### 3. Install Library Python

Buka terminal di VS Code (`Ctrl+\``) lalu jalankan:

```bash
pip install paho-mqtt
```

---

## Struktur Proyek

```
mqtt-smart-room/
├── scenario1_publisher.py              # Skenario 1: publisher dasar
├── scenario1_subscriber.py             # Skenario 1: subscriber dasar
├── scenario2_publisher_qos.py          # Skenario 2: publisher QoS 0, 1, 2
├── scenario2_subscriber_qos.py         # Skenario 2: subscriber semua QoS
├── scenario3_publisher_multitopic.py   # Skenario 3: publisher multi-topik
├── scenario3_subscriber_multitopic.py  # Skenario 3: subscriber multi-topik
├── scenario45_publisher_wildcard.py    # Skenario 4 & 5: publisher wildcard
├── scenario4_subscriber_plus.py        # Skenario 4: subscriber wildcard '+'
├── scenario5_subscriber_hash.py        # Skenario 5: subscriber wildcard '#'
└── README.md
```

---

## Cara Menjalankan di Visual Studio Code

Buka folder proyek di VS Code melalui **File > Open Folder**, lalu pilih folder tempat semua file `.py` disimpan.

Setiap skenario membutuhkan **dua terminal yang berjalan bersamaan**. Buka terminal pertama dengan `Ctrl+\``, lalu buka terminal kedua dengan menekan ikon **+** di panel terminal. Subscriber harus dijalankan lebih dulu sebelum publisher.

### Skenario 1 — Komunikasi Dasar

```bash
# Terminal 1 (jalankan lebih dulu)
python scenario1_subscriber.py

# Terminal 2
python scenario1_publisher.py
```

### Skenario 2 — Variasi QoS

```bash
# Terminal 1 (jalankan lebih dulu)
python scenario2_subscriber_qos.py

# Terminal 2
python scenario2_publisher_qos.py
```

### Skenario 3 — Multi-Topik

```bash
# Terminal 1 (jalankan lebih dulu)
python scenario3_subscriber_multitopic.py

# Terminal 2
python scenario3_publisher_multitopic.py
```

### Skenario 4 — Wildcard `+`

```bash
# Terminal 1 (jalankan lebih dulu)
python scenario4_subscriber_plus.py

# Terminal 2
python scenario45_publisher_wildcard.py
```

### Skenario 5 — Wildcard `#`

```bash
# Terminal 1 (jalankan lebih dulu)
python scenario5_subscriber_hash.py

# Terminal 2
python scenario45_publisher_wildcard.py
```

Untuk menghentikan program, tekan `Ctrl+C` di terminal yang ingin dihentikan.

---

## Struktur Topik MQTT

```
smartroom/
├── sensor/
│   └── basic
├── qos/
│   ├── level0
│   ├── level1
│   └── level2
├── ruang_tamu/
│   ├── temperature
│   ├── humidity
│   ├── motion
│   └── temperature/detail
├── kamar_tidur/
│   ├── temperature
│   ├── light
│   └── light/brightness
├── dapur/
│   ├── co2
│   └── temperature
└── garasi/
    ├── motion
    └── door
```

---

## Perbandingan QoS

| Level | Nama | Jaminan | Cocok Untuk |
|-------|------|---------|-------------|
| 0 | At most once | Tidak ada | Data sensor frekuensi tinggi, toleran kehilangan |
| 1 | At least once | Minimal satu kali, bisa duplikat | Alert dan notifikasi |
| 2 | Exactly once | Tepat satu kali | Perintah kritis, kontrol aktuator |

---

## Perbandingan Wildcard

| Wildcard | Cakupan | Contoh Pattern | Menangkap |
|----------|---------|----------------|-----------|
| `+` | Tepat satu level | `smartroom/+/temperature` | `smartroom/dapur/temperature` — ya |
| `+` | Tepat satu level | `smartroom/+/temperature` | `smartroom/dapur/temperature/detail` — tidak |
| `#` | Semua level di bawah | `smartroom/#` | Semua topik di bawah `smartroom/` |

---

## Pengujian Manual via Terminal

```bash
# Pantau semua topik secara real-time
mosquitto_sub -h localhost -p 1883 -t "#" -v

# Pantau dengan wildcard satu level
mosquitto_sub -h localhost -p 1883 -t "smartroom/+/temperature" -v

# Publish pesan manual untuk pengujian
mosquitto_pub -h localhost -p 1883 -t "smartroom/test" -m "{\"test\": true}"
```

---


- **Broker:** Mosquitto 2.x
- **Bahasa:** Python 3
- **Library:** paho-mqtt
- **Protokol:** MQTT v3.1.1
- **Editor:** Visual Studio Code
