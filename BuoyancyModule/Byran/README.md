# Buoyancy Module Code

### Codebase Overview

`BLEGatt.ino` is the file to be run on the ESP32. The ESP32 becomes a BLE Server, hosting a BLE GATT characteristic with READ, NOTIFY and WRITE properties.

`FrontEnd` is the SvelteKit project to be run on topside. Run `npm run dev` from within `./FrontEnd`. Connect to the ESP32 with the `Connect BLE Device` button. When the `Start Reporting` button is pressed, it will continuously stream data from the ESP32 at ~1hz using the Web Bluetooth API (Chrome 50+ recommended, Safari/Firefox do not work. Edge may work).

Note: To synchronize the time of the ESP32 with the computer, press `Update to Current Time`. Custom UTF-8 encoded text via text input and pressing `Write Custom Text` can also be sent but is not processed.

### Debugging:
nRF Connect iOS/Android App offers many debugging capabilities. Use the UTF-8 encoding.

### TODO:
 - [x] Enable manual resynchronization of UTC time via WRITE property on ESP32
 - [x] Document code
 - [x] Better UI and stream data directy to browser DOM
