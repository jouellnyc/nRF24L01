# nRF24L01 Notes and (AI RF Scanner)

A MicroPython-based spectrum analyzer using the nRF24L01 transceiver to scan and monitor 2.4GHz wireless activity.

## What It Does

This scanner turns your nRF24L01 module into a simple spectrum analyzer for the 2.4GHz ISM band, detecting RF activity from various wireless devices without decoding their actual data.

### Detects Activity From:
- WiFi routers and networks
- Bluetooth devices (frequency hopping patterns)
- 2.4GHz cordless phones
- Wireless mice and keyboards
- Microwave ovens (when running)
- Other nRF24L01 networks
- Various ISM band devices

## Features

- **Full Band Scan**: Monitors all 126 channels (2400-2525 MHz)
- **RF Activity Detection**: Uses carrier detection to sense wireless transmissions
- **Quiet Channel Finder**: Identifies the best channels for interference-free communication
- **Real-time Monitoring**: Continuous scanning with configurable sample duration
- **Signal Strength**: RSSI readings for detected activity

## Hardware Requirements

- ESP32, Raspberry Pi Pico, or any MicroPython-compatible microcontroller
- nRF24L01 transceiver module
- Jumper wires for connections

### Wiring

```
nRF24L01 -> Microcontroller
VCC -> 3.3V
GND -> GND
CE  -> GPIO 6
CSN -> GPIO 5
SCK -> GPIO 2
MOSI-> GPIO 3
MISO-> GPIO 4
```

## Usage

### Basic Scanning
```python
# Initialize scanner
scanner = NRF24L01Scanner()

# Full spectrum scan
scanner.scan_all_channels()

# Find quietest channels for your projects
scanner.find_quiet_channels()

# Monitor specific channel
scanner.monitor_channel(85, duration=30)  # Monitor channel 85 for 30 seconds
```

### Setting Your nRF24L01 to a Clean Channel
```python
# Use scanner results to pick a quiet channel
radio.set_channel(85)  # Set to channel 85 (2485MHz)
```

## Sample Output

```
nRF24L01 2.4GHz Scanner Ready!
========================================
Scanning 2.4GHz band (channels 0-125)...

Channel | Frequency | Activity
--------|-----------|----------
     11 |  2411MHz  |   40.0%  ← WiFi Channel 1
     37 |  2437MHz  |   35.0%  ← WiFi Channel 6  
     62 |  2462MHz  |   45.0%  ← WiFi Channel 11
     85 |  2485MHz  |    0.0%  ← Clean!

Quietest channels for your projects:
1. Channel 85 (2485MHz): 0.0% activity
2. Channel 90 (2490MHz): 0.0% activity
3. Channel 95 (2495MHz): 0.0% activity
```

## Configuration Options

### Sampling Duration
- **10ms**: Quick scan, may miss intermittent signals
- **100ms**: Recommended for reliable results (catches Bluetooth hops)
- **500ms**: Very thorough, good for finding persistent interference

```python
# Adjust sampling time per channel
scanner.scan_all_channels(duration_per_channel=100)  # 100ms per channel
```

## Understanding the Results

### What the Scanner Shows:
- **High activity (>30%)**: Likely WiFi networks or heavy Bluetooth use
- **Scattered random activity**: Bluetooth frequency hopping (normal)
- **Consistent low activity**: Good channels for nRF24L01 projects
- **Zero activity**: Excellent channels for reliable communication

### Common Activity Patterns:
- **Channels 0-25**: Often busy with WiFi and Bluetooth
- **Channels 30-70**: Mixed activity, WiFi channels 1, 6, 11
- **Channels 75-125**: Usually quieter, good for projects

## Limitations

The nRF24L01 scanner has some important constraints:

- **Detection only**: Can sense RF energy but cannot decode WiFi, Bluetooth, or other protocols
- **nRF24L01 band only**: Limited to 2.4GHz ISM band (2400-2525 MHz)
- **No packet decoding**: Shows presence of signals, not their content
- **Simple modulation**: Cannot handle complex modulation schemes

## Use Cases

- **Channel selection**: Find clean channels for your nRF24L01 projects
- **Interference troubleshooting**: Identify sources of wireless interference
- **Network planning**: Visualize 2.4GHz spectrum usage in your area
- **Educational**: Learn about wireless spectrum usage and RF activity
- **IoT deployment**: Choose optimal frequencies for wireless sensor networks

## Installation

1. Copy the scanner code to your MicroPython device
2. Adjust GPIO pin assignments for your hardware
3. Run the scanner and enjoy exploring the 2.4GHz spectrum!

## Tips for Best Results

- Use 100ms sampling duration for reliable detection
- Run multiple scans to see activity patterns over time
- Channels 75-125 often have less interference
- Space multiple nRF24L01 networks 2-3 channels apart
- Avoid channels showing >20% consistent activity

---

*This scanner turns the simple nRF24L01 into a powerful tool for understanding your local 2.4GHz wireless environment!*
