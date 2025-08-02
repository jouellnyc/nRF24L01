"""Simple nRF24L01 communication functions for Pi Pico"""

import struct
import utime
from machine import Pin, SPI
from .nrf24l01 import NRF24L01

# Your proven working configuration
def setup_nrf(role="sender"):
    """Setup nRF24L01 with your proven reliable settings"""
    spi = SPI(0, sck=Pin(2), mosi=Pin(3), miso=Pin(4))
    csn = Pin(5, mode=Pin.OUT, value=1)
    ce = Pin(6, mode=Pin.OUT, value=0)
    
    nrf = NRF24L01(spi, csn, ce, payload_size=32)  # 32 bytes payload
    
    # Your proven reliable settings
    nrf.reg_write(0x06, 0x27)  # 250kbps, 0dBm power 
    nrf.reg_write(0x01, 0x00)  # Disable auto-ack
    nrf.reg_write(0x04, 0xFF)  # Max retries (though not used with auto-ack off)
    
    # Addresses (same as your test)
    addr1 = b"\xe1\xf0\xf0\xf0\xf0"
    addr2 = b"\xd2\xf0\xf0\xf0\xf0"
    
    if role == "sender":
        nrf.open_tx_pipe(addr1)
        nrf.open_rx_pipe(1, addr2)  # For receiving acks if needed
    else:  # receiver
        nrf.open_tx_pipe(addr2)
        nrf.open_rx_pipe(1, addr1)
        nrf.start_listening()
    
    return nrf

# Simple sending functions
def send_string(nrf, message, max_retries=3):
    """Send a string message with automatic retries"""
    data = message.encode('utf-8')[:32]  # Truncate to 32 bytes
    data = data + b'\x00' * (32 - len(data))  # Pad with zeros to 32 bytes
    
    for attempt in range(max_retries):
        try:
            nrf.stop_listening()
            nrf.send(data)
            print(f"Sent: '{message}' (attempt {attempt + 1})")
            return True
        except OSError as e:
            print(f"Send attempt {attempt + 1} failed: {e}")
            utime.sleep_ms(50)
    
    print(f"Failed to send after {max_retries} attempts")
    return False

def send_numbers(nrf, *numbers, max_retries=3):
    """Send up to 8 integers (32 bytes total)"""
    if len(numbers) > 8:
        numbers = numbers[:8]  # Limit to 8 integers
    
    # Pack integers into bytes
    format_str = 'i' * len(numbers)  # 'i' = 4 bytes per integer
    data = struct.pack(format_str, *numbers)
    data = data + b'\x00' * (32 - len(data))  # Pad to 32 bytes
    
    for attempt in range(max_retries):
        try:
            nrf.stop_listening()
            nrf.send(data)
            print(f"Sent numbers: {numbers} (attempt {attempt + 1})")
            return True
        except OSError as e:
            print(f"Send attempt {attempt + 1} failed: {e}")
            utime.sleep_ms(50)
    
    print(f"Failed to send after {max_retries} attempts")
    return False

def send_sensor_data(nrf, temperature=None, humidity=None, pressure=None, max_retries=3):
    """Send sensor data as floats"""
    # Pack as floats (4 bytes each)
    data = struct.pack('fff', 
                      temperature or 0.0, 
                      humidity or 0.0, 
                      pressure or 0.0)
    data = data + b'\x00' * (32 - len(data))  # Pad to 32 bytes
    
    for attempt in range(max_retries):
        try:
            nrf.stop_listening()
            nrf.send(data)
            print(f"Sent sensor data: T={temperature}, H={humidity}, P={pressure} (attempt {attempt + 1})")
            return True
        except OSError as e:
            print(f"Send attempt {attempt + 1} failed: {e}")
            utime.sleep_ms(50)
    
    print(f"Failed to send after {max_retries} attempts")
    return False

# Simple receiving functions
def receive_string(nrf, timeout_ms=1000):
    """Receive a string message"""
    start_time = utime.ticks_ms()
    
    while utime.ticks_diff(utime.ticks_ms(), start_time) < timeout_ms:
        if nrf.any():
            data = nrf.recv()
            # Convert bytes back to string, removing padding
            try:
                message = data.rstrip(b'\x00').decode('utf-8')
                print(f"Received: '{message}'")
                return message
            except:
                print("Received invalid UTF-8 data")
                return None
        utime.sleep_ms(1)
    
    return None  # Timeout

def receive_numbers(nrf, count=8, timeout_ms=1000):
    """Receive up to 8 integers"""
    start_time = utime.ticks_ms()
    
    while utime.ticks_diff(utime.ticks_ms(), start_time) < timeout_ms:
        if nrf.any():
            data = nrf.recv()
            # Unpack integers
            format_str = 'i' * count
            try:
                numbers = struct.unpack(format_str, data[:count*4])
                print(f"Received numbers: {numbers}")
                return numbers
            except struct.error:
                print("Error unpacking numbers")
                return None
        utime.sleep_ms(1)
    
    return None  # Timeout

def receive_sensor_data(nrf, timeout_ms=1000):
    """Receive sensor data as floats"""
    start_time = utime.ticks_ms()
    
    while utime.ticks_diff(utime.ticks_ms(), start_time) < timeout_ms:
        if nrf.any():
            data = nrf.recv()
            try:
                temp, humidity, pressure = struct.unpack('fff', data[:12])
                print(f"Received sensor data: T={temp:.1f}, H={humidity:.1f}, P={pressure:.1f}")
                return {'temperature': temp, 'humidity': humidity, 'pressure': pressure}
            except struct.error:
                print("Error unpacking sensor data")
                return None
        utime.sleep_ms(1)
    
    return None  # Timeout

# Example usage functions
def sender_example():
    """Example sender code"""
    print("Setting up sender...")
    nrf = setup_nrf("sender")
    
    print("Sending different types of data...")
    
    # Send strings
    send_string(nrf, "Hello World!")
    utime.sleep_ms(500)
    
    # Send numbers
    send_numbers(nrf, 42, 123, 456)
    utime.sleep_ms(500)
    
    # Send sensor data
    send_sensor_data(nrf, temperature=23.5, humidity=65.2, pressure=1013.25)
    utime.sleep_ms(500)
    
    print("Sender example complete")

def receiver_example():
    """Example receiver code"""
    print("Setting up receiver...")
    nrf = setup_nrf("receiver")
    
    print("Listening for data... (Ctrl-C to stop)")
    
    while True:
        # Try to receive different types of data
        message = receive_string(nrf, timeout_ms=100)
        if message:
            continue
            
        numbers = receive_numbers(nrf, timeout_ms=100)
        if numbers:
            continue
            
        sensor_data = receive_sensor_data(nrf, timeout_ms=100)
        if sensor_data:
            continue
        
        utime.sleep_ms(10)  # Small delay to prevent busy waiting

print("nRF24L01 simple usage functions loaded!")
print("Usage:")
print("  sender_example()    - Run sender example")
print("  receiver_example()  - Run receiver example")
print("  Or use individual functions like send_string(), receive_string(), etc.")