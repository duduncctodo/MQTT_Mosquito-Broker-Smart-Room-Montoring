# Smart Room Monitoring — MQTT Communication System

A Python-based MQTT communication system simulating a smart room environment. Built using Mosquitto as the message broker and `paho-mqtt` as the client library, this project demonstrates the publish-subscribe pattern across five scenarios covering basic communication, QoS levels, multi-topic publishing, and wildcard subscriptions.

Developed as part of a Cyber Physical Systems lab assignment.

---

## Overview

The system simulates sensor data from multiple rooms (living room, bedroom, kitchen, garage), each publishing different sensor readings to a structured topic hierarchy. Subscribers filter messages using explicit topics or MQTT wildcards.

**Scenarios covered:**

| # | Scenario | Description |
|---|----------|-------------|
| 1 | Basic pub-sub | Publisher sends temperature and humidity data; subscriber receives and displays it |
| 2 | QoS levels | Same data sent at QoS 0, 1, and 2 to compare delivery guarantees |
| 3 | Multi-topic | Six sensor types across three rooms, each on its own topic |
| 4 | Wildcard `+` | Single-level wildcard matching one segment of a topic path |
| 5 | Wildcard `#` | Multi-level wildcard capturing all subtopics under a prefix |

---

## Requirements

- Python 3.7+
- Mosquitto MQTT Broker
- paho-mqtt

```bash
pip install paho-mqtt
```

**Installing Mosquitto:**

```bash
# Ubuntu / Debian
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

**Mosquitto configuration** — create or edit `/etc/mosquitto/conf.d/local.conf`:

```
listener 1883 localhost
allow_anonymous true
```

Restart after editing:

```bash
sudo systemctl restart mosquitto
```

---

## Project Structure

```
mqtt-smart-room/
├── scenario1_publisher.py              # Basic publisher
├── scenario1_subscriber.py             # Basic subscriber
├── scenario2_publisher_qos.py          # Publisher with QoS 0, 1, 2
├── scenario2_subscriber_qos.py         # Subscriber for all QoS levels
├── scenario3_publisher_multitopic.py   # Multi-topic publisher
├── scenario3_subscriber_multitopic.py  # Multi-topic subscriber
├── scenario45_publisher_wildcard.py    # Publisher for wildcard testing
├── scenario4_subscriber_plus.py        # Wildcard '+' subscriber
├── scenario5_subscriber_hash.py        # Wildcard '#' subscriber
└── README.md
```

---

## Running the Scenarios

Start the subscriber first in one terminal, then the publisher in a second terminal. The subscriber must be running before the publisher sends messages, otherwise messages sent before the subscription is active will be missed (for QoS 0).

### Scenario 1 — Basic Communication

```bash
# Terminal 1
python3 scenario1_subscriber.py

# Terminal 2
python3 scenario1_publisher.py
```

### Scenario 2 — QoS Levels

```bash
# Terminal 1
python3 scenario2_subscriber_qos.py

# Terminal 2
python3 scenario2_publisher_qos.py
```

### Scenario 3 — Multiple Topics

```bash
# Terminal 1
python3 scenario3_subscriber_multitopic.py

# Terminal 2
python3 scenario3_publisher_multitopic.py
```

### Scenario 4 — Wildcard `+`

```bash
# Terminal 1
python3 scenario4_subscriber_plus.py

# Terminal 2
python3 scenario45_publisher_wildcard.py
```

### Scenario 5 — Wildcard `#`

```bash
# Terminal 1
python3 scenario5_subscriber_hash.py

# Terminal 2
python3 scenario45_publisher_wildcard.py
```

Stop any running script with `Ctrl+C`.

---

## Topic Structure

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

## QoS Reference

| Level | Name | Guarantee | Use Case |
|-------|------|-----------|----------|
| 0 | At most once | No guarantee | High-frequency sensor data where occasional loss is acceptable |
| 1 | At least once | Delivered at least once, may duplicate | Alerts and notifications |
| 2 | Exactly once | Delivered exactly once | Critical commands, actuator control |

---

## Wildcard Reference

| Wildcard | Matches | Example | Catches |
|----------|---------|---------|---------|
| `+` | Exactly one level | `smartroom/+/temperature` | `smartroom/dapur/temperature` |
| `+` | Exactly one level | `smartroom/+/temperature` | `smartroom/dapur/temperature/detail` — no |
| `#` | All levels below | `smartroom/#` | Everything under `smartroom/` |

---

## Manual Testing with CLI

```bash
# Subscribe to all topics (useful for debugging)
mosquitto_sub -h localhost -p 1883 -t "#" -v

# Subscribe with single-level wildcard
mosquitto_sub -h localhost -p 1883 -t "smartroom/+/temperature" -v

# Publish a test message manually
mosquitto_pub -h localhost -p 1883 -t "smartroom/test" -m '{"test": true}'
```

---

## Tech Stack

- **Broker:** Mosquitto 2.x
- **Language:** Python 3
- **Library:** paho-mqtt
- **Protocol:** MQTT v3.1.1
