import time
import machine
from machine import Pin, SPI

class NRF24L01:
    """Basic nRF24L01 driver for scanning"""

    # Register addresses
    CONFIG = 0x00
    EN_AA = 0x01
    EN_RXADDR = 0x02
    SETUP_AW = 0x03
    SETUP_RETR = 0x04
    RF_CH = 0x05
    RF_SETUP = 0x06
    STATUS = 0x07
    OBSERVE_TX = 0x08
    RPD = 0x09  # Received Power Detector

    # Commands
    R_REGISTER = 0x00
    W_REGISTER = 0x20
    R_RX_PAYLOAD = 0x61
    W_TX_PAYLOAD = 0xA0
    FLUSH_TX = 0xE1
    FLUSH_RX = 0xE2
    REUSE_TX_PL = 0xE3
    NOP = 0xFF

    def __init__(self, spi, cs, ce):
        self.spi = spi
        self.cs = cs
        self.ce = ce
        self.cs.init(Pin.OUT, value=1)
        self.ce.init(Pin.OUT, value=0)
        time.sleep_ms(100)
        self.init_radio()

    def write_register(self, reg, value):
        """Write to a register"""
        self.cs.value(0)
        self.spi.write(bytearray([self.W_REGISTER | reg, value]))
        self.cs.value(1)

    def read_register(self, reg):
        """Read from a register"""
        self.cs.value(0)
        self.spi.write(bytearray([self.R_REGISTER | reg]))
        result = self.spi.read(1)
        self.cs.value(1)
        return result[0]

    def init_radio(self):
        """Initialize the radio for scanning"""
        # Power up in RX mode
        self.write_register(self.CONFIG, 0x0B)  # PWR_UP=1, PRIM_RX=1

        # Disable auto-acknowledge
        self.write_register(self.EN_AA, 0x00)

        # Enable RX pipe 0
        self.write_register(self.EN_RXADDR, 0x01)

        # Set address width to 5 bytes
        self.write_register(self.SETUP_AW, 0x03)

        # Set RF power to max and data rate to 2Mbps
        self.write_register(self.RF_SETUP, 0x0F)

        time.sleep_ms(150)  # Wait for power up

    def set_channel(self, channel):
        """Set RF channel (0-125)"""
        if 0 <= channel <= 125:
            self.write_register(self.RF_CH, channel)

    def start_listening(self):
        """Start listening mode"""
        self.ce.value(1)
        time.sleep_us(130)  # Minimum RX settling time

    def stop_listening(self):
        """Stop listening mode"""
        self.ce.value(0)

    def test_carrier(self):
        """Test for carrier detect (RPD bit)"""
        # Read the RPD (Received Power Detector) register
        rpd = self.read_register(self.RPD)
        return rpd & 0x01  # RPD bit is bit 0

class RF_Scanner:
    """2.4GHz RF Scanner using nRF24L01"""

    def __init__(self, radio):
        self.radio = radio
        self.scan_results = {}

    def scan_single_channel(self, channel, duration_ms=10):
        """Scan a single channel for activity"""
        self.radio.set_channel(channel)
        self.radio.start_listening()

        # Sample multiple times for better detection
        detections = 0
        samples = max(1, duration_ms // 2)

        for _ in range(samples):
            if self.radio.test_carrier():
                detections += 1
            time.sleep_ms(2)

        self.radio.stop_listening()

        # Return detection percentage
        return (detections / samples) * 100

    """
    To get clearer results, try:
    python# Longer sampling per channel
    scanner.scan_all_channels(duration_per_channel=100)  # 100ms instead of 10ms

    # Or multiple scans to see patterns
    for i in range(5):
        print(f"\n--- Scan {i+1} ---")
        scanner.scan_all_channels(20)
        time.sleep(2)
    """

    def scan_all_channels(self, duration_per_channel=100):
        """Scan all 126 channels"""
        print("Scanning 2.4GHz band (channels 0-125)...")
        print("Channel | Frequency | Activity")
        print("--------|-----------|----------")

        active_channels = []

        for channel in range(126):
            frequency = 2400 + channel
            activity = self.scan_single_channel(channel, duration_per_channel)

            if activity > 0:
                active_channels.append((channel, frequency, activity))
                print(f"{channel:7} | {frequency:8}MHz | {activity:6.1f}%")

        return active_channels

    def continuous_scan(self, channels=None, update_interval=1):
        """Continuously scan specified channels"""
        if channels is None:
            # Default to WiFi channels (approximate)
            channels = [1, 6, 11, 36, 40, 44, 48, 52, 56, 60, 64]

        print(f"Continuous scanning channels: {channels}")
        print("Press Ctrl+C to stop")

        try:
            while True:
                print(f"\n--- Scan at {time.ticks_ms()} ms ---")
                for channel in channels:
                    activity = self.scan_single_channel(channel)
                    freq = 2400 + channel
                    status = "ACTIVE" if activity > 10 else "quiet"
                    print(f"Ch{channel:3} ({freq}MHz): {activity:5.1f}% {status}")

                time.sleep(update_interval)

        except KeyboardInterrupt:
            print("\nScan stopped")

    def find_quiet_channel(self, channels=None):
        """Find the quietest channel for your own communications"""
        if channels is None:
            channels = list(range(0, 126, 5))  # Sample every 5th channel

        print("Finding quietest channel...")
        results = []

        for channel in channels:
            activity = self.scan_single_channel(channel, 50)  # Longer scan
            results.append((channel, activity))
            print(f"Channel {channel}: {activity:.1f}% activity")

        # Sort by activity level
        results.sort(key=lambda x: x[1])

        print(f"\nQuietest channels:")
        for i, (channel, activity) in enumerate(results[:5]):
            freq = 2400 + channel
            print(f"{i+1}. Channel {channel} ({freq}MHz): {activity:.1f}% activity")

        return results[0][0]  # Return quietest channel

# Main usage example
def main():
    # Initialize SPI and pins (adjust for your board)
    # Common pin configurations:
    # ESP32: SCK=18, MOSI=23, MISO=19, CS=5, CE=4
    # Raspberry Pi Pico: SCK=2, MOSI=3, MISO=4, CS=5, CE=6
    spi = SPI(0, baudrate=4000000, polarity=0, phase=0,
              sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    cs = Pin(5)
    ce = Pin(6)

    try:
        # Initialize radio
        radio = NRF24L01(spi, cs, ce)
        scanner = RF_Scanner(radio)

        print("nRF24L01 2.4GHz Scanner Ready!")
        print("=" * 40)

        # Quick scan of all channels
        active = scanner.scan_all_channels()

        if active:
            print(f"\nFound activity on {len(active)} channels")
            print("Top active channels:")
            active.sort(key=lambda x: x[2], reverse=True)
            for channel, freq, activity in active[:10]:
                print(f"  Channel {channel} ({freq}MHz): {activity:.1f}%")
        else:
            print("\nNo significant activity detected")

        # Find quiet channel for your own use
        print("\n" + "=" * 40)
        quiet_ch = scanner.find_quiet_channel()
        print(f"\nRecommended channel for your projects: {quiet_ch}")

        # Uncomment for continuous monitoring
        # print("\n" + "=" * 40)
        # scanner.continuous_scan()

    except Exception as e:
        print(f"Error: {e}")
        print("Check your wiring and connections")

if __name__ == "scan":
    main()

