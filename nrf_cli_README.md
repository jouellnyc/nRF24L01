# nrf_cli.py  Usage Examples

## Setup and Import

```python
from nrf24l01 import nrf_cli as r

# nRF24L01 simple usage functions loaded!
# Usage:
#   sender_example()    - Run sender example
#   receiver_example()  - Run receiver example
#   Or use individual functions like send_string(), receive_string(), etc.
```

## Receiving Numbers

```python
# Setup receiver
nrf = r.setup_nrf("receiver")

# Continuously receive numbers
while True:
    message = r.receive_numbers(nrf)
    if message:
        print(f"Got: {message}")
```

**Example Output:**
```
Received numbers: (1819043144, 8559, 0, 0, 0, 0, 0, 0)
Got: (1819043144, 8559, 0, 0, 0, 0, 0, 0)

Received numbers: (1819043144, 111, 0, 0, 0, 0, 0, 0)
Got: (1819043144, 111, 0, 0, 0, 0, 0, 0)

Received numbers: (1819043144, 24943, 0, 0, 0, 0, 0, 0)
Got: (1819043144, 24943, 0, 0, 0, 0, 0, 0)
```

## Receiving Strings

```python
# Setup receiver
nrf = r.setup_nrf("receiver")

# Continuously receive strings
while True:
    message = r.receive_string(nrf)
    if message:
        print(f"Got: {message}")
```

**Example Output:**
```
Received: 'Hello!'
Got: Hello!
```

## Available Functions

- `r.setup_nrf("receiver")` - Initialize nRF24L01 as receiver
- `r.setup_nrf("sender")` - Initialize nRF24L01 as sender  
- `r.receive_numbers(nrf)` - Receive tuple of numbers
- `r.receive_string(nrf)` - Receive string messages
- `sender_example()` - Run built-in sender example
- `receiver_example()` - Run built-in receiver example

## Notes

- Use `Ctrl+C` to interrupt the receiving loop
- The `receive_text()` function does not exist - use `receive_string()` instead
- Messages are received continuously in a blocking loop
