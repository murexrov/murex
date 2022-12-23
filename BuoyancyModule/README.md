# Buoyancy Module Code

`BLEGatt.ino` is the file to be run on the ESP32. The ESP32 becomes a BLE Server, hosting a BLE GATT characteristic with READ, NOTIFY and WRITE properties.

`index.html` is the file to be run on topside. Connect to the ESP32 with the `Connect` button. When the `start` button is pressed, it will continuously stream data from the ESP32 at ~1hz using the Web Bluetooth API (Chrome 50+ recommended, Safari/Firefox do not work. Edge may work). The data is accessed over the "inspect element" console.

TODO:
 - [ ] Enable manual resynchronization of UTC time via WRITE property on ESP32
 - [ ] Document code
 - [ ] Better UI and stream data directy to browser DOM
