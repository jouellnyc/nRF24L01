# nRF24L01 Notes and (AI RF Scanner)
A MicroPython-based spectrum analyzer using the nRF24L01 transceiver to scan and monitor 2.4GHz wireless activity.

## A Curious Adventure

I came across these modules to use in a project and tryed to get them installed and working. I bought six of them from AliExpress.<BR>
Cheap, some $1, some 50 cents US. Having not used these I always keep risk low the first time.  :)
<P>
It turns out that some of them were definitely "counterfeit" and it appears that some were "legitimate". <BR>
I'm using those terms loosely --  that is to say some of them worked and some of them straight up didn't. 
<P>
The ones that did work  had  mapping of the gpios on them:<BR>
<img width="320" height="426" alt="image" src="https://github.com/user-attachments/assets/9dcd3857-6e33-4ec6-8590-af6879ef0bb0" />
<P></P>
The ones that did not were just blank:<BR>
<img width="320" height="426" alt="image" src="https://github.com/user-attachments/assets/d00b239c-ebd1-43fc-ad93-b9ab507850bf" />

Only problem is each listing on the site showed them as blank and I don't see a way to order 'the good ones'. That being the case, when  I tried to use the ones that were working I only  ot  about 25% success transmission at first -- at about 12-18 inches distance. With help of Claude AI,  I was able to come up with some optimizations that got them  working to a place of about 75%-85% successful transmissions - I played around to about 5 feet distance - no issues.
<P></P>
I hope this information helps.  The code and the optimizations are included as `nrf24_tuned_test.py`.
<P>
It's mostly these:

```
 nrf.reg_write(0x06, 0x27)  # RF_SETUP: 250kbps, 0dBm power 
 nrf.reg_write(0x01, 0x00)  # Disable auto-ack on all pipes
 nrf.reg_write(0x04, 0xFF)  # SETUP_RETR: max delay, 15 retries
```
and some of the initial delays. Yes, the product is now weakened version BUT I get to play w/the toy now :).
I also tried a 10 µF and 47 µF capacitor between VCC/GND on each module.  47 µF seemed to work best.

Just my experience - I have about 24 hours worth of 'expertise',  so grain of salt here.

Being curious I asked Claude to write a scanner. It's here as 'scan.py'. So grain of salt here, but seems to work well.



## What scan.py Does

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
- Space multiple nRF24L01 networks 2-3 channels apart
- Avoid channels showing >20% consistent activity

## References
- https://coffeebreakpoint.com/micropython/how-to-connect-a-nrf24l01-transceiver-to-your-raspberry-pi-pico/
- https://github.com/orgs/micropython/discussions/10155
---

*This scanner turns the simple nRF24L01 into a powerful tool for understanding your local 2.4GHz wireless environment!*
