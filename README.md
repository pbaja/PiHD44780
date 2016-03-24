# Features

 - Super lightweight (Only ONE 3.8KB file!)
 - Really fast (Using Hardware i<sup>2</sup>c)
 - Tested on 2x16 and 4x20
 - Cool "loading" animation

# Usage

1. Enable I2C interface with raspi-config
   - In console execute "raspi-config"
   - Select Advanced Options, I2C, Yes, Ok, Yes, Ok
   - With right arrow key select Finish and select Yes for reboot now.
   - After reboot I2C should be enabled

3. Install python library and tools

    ```
    apt-get install python-smbus i2c-tools git-core
    ```

4. Connect LCD
   - GND to GND
   - VCC to 5V
   - SDA to SDA (GPIO2)
   - SCL to SCL (GPIO3)

5. Reboot raspberry to changes take effect

6. Check LCD address, mine is 0x27

    ```
    i2cdetect -y 1
    ```

7. Download library and run example.py

    ```
    git clone https://github.com/SkewPL/LimeLCD.git
    cd LimeLCD
    python example.py
    ```
