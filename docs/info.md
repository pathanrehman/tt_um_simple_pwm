<!---
This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.
You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

# SimplePWM - Basic PWM Generator

**SimplePWM** is a straightforward 8-bit Pulse Width Modulation (PWM) generator designed for beginners learning digital design. This project creates variable-duty-cycle square wave signals perfect for LED brightness control, motor speed regulation, and basic analog signal generation.

## How it works

SimplePWM uses a classic counter-comparator architecture to generate PWM signals with 256 different duty cycle levels.

### Core Architecture

The PWM generator consists of three main components:

1. **8-bit Counter**: Continuously counts from 0 to 255, then rolls over to 0
2. **Comparator Logic**: Compares the counter value with the duty cycle input  
3. **Output Generator**: Produces the PWM signal based on the comparison

### PWM Generation Process

The PWM signal is generated using this simple algorithm:
- **When counter < duty_cycle**: PWM output = HIGH (1)
- **When counter ≥ duty_cycle**: PWM output = LOW (0)

This creates a periodic square wave where the percentage of time spent HIGH equals the duty cycle percentage.

### Timing and Frequency

- **PWM Period**: 256 clock cycles (full counter cycle)
- **PWM Frequency**: Clock frequency ÷ 256
- **Resolution**: 8-bit (256 discrete duty cycle levels)
- **Duty Cycle Range**: 0% to 99.6% (0/256 to 255/256)

### Example Operation

For a 10 MHz input clock:
- **PWM Frequency**: 10 MHz ÷ 256 = 39.06 kHz
- **PWM Period**: 25.6 µs
- **50% Duty Cycle** (duty_cycle = 128): HIGH for 12.8 µs, LOW for 12.8 µs

## How to test

### Basic Setup

1. **Connect Power**: Ensure your TinyTapeout demo board is powered and the design is selected
2. **Set Duty Cycle**: Use the 8-bit input switches (ui_in[7:0]) to set desired duty cycle value
3. **Observe Output**: Monitor the PWM signal on output pin uo_out[0]

### Test Sequences

#### LED Brightness Test
1. Connect an LED with appropriate current-limiting resistor to uo_out[0]
2. Test different duty cycle values:
   - **0x00 (0)**: LED completely OFF
   - **0x40 (64)**: LED at 25% brightness  
   - **0x80 (128)**: LED at 50% brightness
   - **0xC0 (192)**: LED at 75% brightness
   - **0xFF (255)**: LED at maximum brightness

#### Oscilloscope Verification
1. Connect oscilloscope probe to uo_out[0]
2. Set duty cycle to 128 (50%)
3. Verify:
   - Square wave present at ~39 kHz
   - Duty cycle approximately 50%
   - Signal swings between 0V and supply voltage

#### Debug Counter Observation
Monitor the counter bits on outputs uo_out[7:1] to verify counter operation:
- **uo_out[1]**: Counter bit 0 (fastest changing bit)
- **uo_out[7]**: Counter bit 6 (slowest changing bit)

### Test Cases

| Duty Cycle Input | Hex | Decimal | Expected LED Brightness | PWM HIGH Time |
|------------------|-----|---------|------------------------|---------------|
| 00000000 | 0x00 | 0 | OFF (0%) | 0/256 of cycle |
| 00010000 | 0x10 | 16 | Very dim (6.25%) | 16/256 of cycle |
| 01000000 | 0x40 | 64 | Dim (25%) | 64/256 of cycle |
| 10000000 | 0x80 | 128 | Medium (50%) | 128/256 of cycle |
| 11000000 | 0xC0 | 192 | Bright (75%) | 192/256 of cycle |
| 11111111 | 0xFF | 255 | Almost full (99.6%) | 255/256 of cycle |

## External hardware

### Required Components

1. **TinyTapeout Demo Board**
   - Provides power, clock, and I/O interface
   - Input switches for duty cycle control
   - Standard TinyTapeout project selection

2. **LED Test Circuit**
   - Standard LED (any color, 3mm or 5mm)
   - Current limiting resistor (220Ω to 1kΩ recommended)
   - Connect: uo_out[0] → Resistor → LED → GND

3. **Oscilloscope (Optional)**
   - For signal verification and measurement
   - Connect probe to uo_out[0]
   - Ground clip to demo board ground

### Advanced Test Hardware

1. **Motor Speed Control**
   - Small DC motor (3-6V)
   - NPN transistor (2N2222 or similar) for current amplification
   - Flyback diode for motor protection
   - Circuit: PWM → Transistor base → Motor control

2. **Analog Voltage Generation**
   - RC low-pass filter: 1kΩ resistor + 10µF capacitor
   - Creates smooth DC voltage proportional to duty cycle
   - Output voltage ≈ (duty_cycle/255) × supply voltage

3. **Audio Generation**
   - RC filter + small speaker/buzzer
   - Low-pass filter smooths PWM into audio signal
   - Vary duty cycle for different tone intensities

### Pin Connections

- **ui_in[7:0]**: Connect to 8-bit DIP switch or input controls
- **uo_out[0]**: Main PWM output - connect to LED, motor driver, or scope
- **uo_out[7:1]**: Counter debug outputs - optional scope connections
- **Power/Ground**: Standard TinyTapeout demo board connections

This SimplePWM project provides an excellent introduction to PWM concepts while demonstrating practical applications in LED control, motor driving, and signal generation.
