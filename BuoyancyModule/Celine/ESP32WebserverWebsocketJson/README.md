# ESP32WebserverWebsocketJson

## Codebase Overview
This is a JSON webserver for the ESP32 which includes websockets and JSON encapsulation for exchange of multiple variables (currently it only displays time, but we can add team number later). It uses the ESP32's internal RTC to get time.

## Expected Behavior
Upload the INO to the ESP32 and compile. Open a standard browser and navigate to the IP address from the udp code in Previous Code. This will show the current time from the computer.

## Troubleshooting
The ESP32 only supports 2.4G networks. 5G networks will not be seen by the ESP32.