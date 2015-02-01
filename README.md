# Features

 - Super lightweight (Only ONE 3.8KB file!)
 - Really fast (Using Hardware i<sup>2</sup>c)
 - Tested on 2x16 and 4x20
 - Cool "loading" animation

# Usage

1. Add these two lines at end of the "/etc/modules" file:

    ```
    i2c-bcm2708 
    i2c-dev
    ```

2. Be sure to comment out these two lines in "/etc/modprobe.d/raspi-blacklist.conf"

    ```
    blacklist spi-bcm2708
    blacklist i2c-bcm2708
    ```

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
