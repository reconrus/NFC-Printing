## Required Libraries 
https://github.com/miguelbalboa/rfid <br>
https://github.com/esp8266/Arduino

## Wiring

|MFRC522|ESP8266 (ESP-12)| NodeMcu v3 Lua |
|--|--|--|
| SDA(SS)| GPIO4  | D2 |
| SCK    | GPIO14 | D5 |
| MOSI   | GPIO13 | D7 |
| MISO   | GPIO12 | D6 |
| GND    | GND    | G  |
| RST    | GPIO5  | D1 |
| 3.3V   | 3.3V	  | 3V |


## Constants
 
chipID - ID of the chip attached to the printer (Strictly 4 characters *for now*) <br>
ssid - SSID of the Wi-Fi Network <br>
pass - Password of the Wi-Fi Network <br> 
serverAddress - IP address + port of the server 
