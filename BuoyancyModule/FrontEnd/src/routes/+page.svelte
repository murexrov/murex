<div class="absolute flex flex-col w-screen py-10 items-center justify-center font-medium text-3xl text-neutral-200">
  <h1>MUREX ROV Buoyancy Module Topside Control</h1>
  <h1 class="text-lg font-normal">ESP32 with BLE GATT, Custom 128-bit UUID Service</h1>
  <h1 class="text-lg font-normal">Chrome 58+, Bluetooth Web API</h1>
</div>

<div class="absolute flex w-screen h-2/3 items-center justify-center">
  <button id="read">Connect BLE Device</button>
  <button id="start" disabled>Start Reporting</button>
  <button id="stop" disabled>Stop Reporting</button>
  <button id="write">Write Custom Text</button>
  <input id="input" placeholder="custom text input"/>
  <button id="writeCurrentTime">Update to Current Time</button>
</div>

<div class="flex w-screen h-screen items-center justify-center font-bold text-4xl text-neutral-200">
  <h1>{output}</h1>
</div>

<script lang="js">
	import { onMount } from 'svelte';
	import "../app.css";
  // Change name based on ESP32 device name, will filter to only matching name device
  var deviceName = 'ESP32 Byran'
  var bleService = '1aade6e4-c95a-419f-bcd7-6ab375f19e01'
  var bleCharacteristic = 'fcfcad0b-035c-49e7-a828-ef109bce0682'
  /**
	 * @type {{ gatt: { connected: any; connect: () => Promise<any>; }; }}
	 */
  var bluetoothDeviceDetected
  /**
	 * @type {{ writeValue: (arg0: Uint8Array) => any; readValue: () => any; addEventListener: (arg0: string, arg1: (event: any) => void) => void; startNotifications: () => Promise<any>; stopNotifications: () => Promise<any>; }}
	 */
  var gattCharacteristic
	/**
	 * @type {string}
	 */
	var output = "No Bluetooth Device Connected..."

	onMount(() => {
		document.querySelector('#read').addEventListener('click', function() {
    if (isWebBluetoothEnabled()) { read() }
  })

  document.querySelector('#start').addEventListener('click', function(event) {
    if (isWebBluetoothEnabled()) { start() }
  })

  document.querySelector('#stop').addEventListener('click', function(event) {
    if (isWebBluetoothEnabled()) { stop() }
  })

  document.querySelector('#write').addEventListener('click', function(event) {
    if (isWebBluetoothEnabled()) { write(document.querySelector('#input').value) }
  })

  document.querySelector('#writeCurrentTime').addEventListener('click', function(event) {
    if (isWebBluetoothEnabled()) { write(new Date(Date.now()).getUTCHours() + " " + new Date(Date.now()).getUTCMinutes() + " " + new Date(Date.now()).getUTCSeconds() + " ") }
  })
	});

  function isWebBluetoothEnabled() {
    if (!navigator.bluetooth) {
      console.log('Web Bluetooth API is not available in this browser!')
      return false
    }

    return true
  }

  function getDeviceInfo() {
    let options = {
      optionalServices: [bleService],
      filters: [
        { "name": deviceName }
      ]
    }

    console.log('Requesting any Bluetooth Device...')
    return navigator.bluetooth.requestDevice(options).then(device => {
      bluetoothDeviceDetected = device
    }).catch(error => {
      console.log('Argh! ' + error)
    })
  }

  function write(value) {
    let encoder = new TextEncoder('utf-8');
    let array = encoder.encode(value);
    // gattCharacteristic.writeValue(array);
    return (bluetoothDeviceDetected ? Promise.resolve() : getDeviceInfo())
    .then(connectGATT)
    .then(_ => {
      console.log('Writing Custom Characteristic...')
      return gattCharacteristic.writeValue(array)
    })
    .catch(error => {
      console.log('[ERROR] Waiting to start writing: ' + error)
    })
  }

  function read() {
    return (bluetoothDeviceDetected ? Promise.resolve() : getDeviceInfo())
    .then(connectGATT)
    .then(_ => {
      console.log('Reading Custom Characteristic...')
      return gattCharacteristic.readValue()
    })
    .catch(error => {
      console.log('Waiting to start reading: ' + error)
    })
  }

  function connectGATT() {
    if (bluetoothDeviceDetected.gatt.connected && gattCharacteristic) {
      return Promise.resolve()
    }

    return bluetoothDeviceDetected.gatt.connect()
    .then(server => {
      console.log('Getting GATT Service...')
      return server.getPrimaryService(bleService)
    })
    .then(service => {
      console.log('Getting GATT Characteristic...')
      return service.getCharacteristic(bleCharacteristic)
    })
    .then(characteristic => {
      gattCharacteristic = characteristic
      gattCharacteristic.addEventListener('characteristicvaluechanged',
          handleChangedValue)
      document.querySelector('#start').disabled = false
      document.querySelector('#stop').disabled = true
    })
  }

  function handleChangedValue(event) {
    let value = event.target.value
    var now = new Date()
		$: output = new TextDecoder("utf-8").decode(value)
    console.log('> ' + now.getHours() + ':' + now.getMinutes() + ':' + now.getSeconds() + ' Value is ' + new TextDecoder("utf-8").decode(value))
  }

  function start() {
    gattCharacteristic.startNotifications()
    .then(_ => {
      console.log('Start reading...')
      document.querySelector('#start').disabled = true
      document.querySelector('#stop').disabled = false
    })
    .catch(error => {
      console.log('[ERROR] Start: ' + error)
    })
  }

  function stop() {
    gattCharacteristic.stopNotifications()
    .then(_ => {
      console.log('Stop reading...')
      document.querySelector('#start').disabled = false
      document.querySelector('#stop').disabled = true
    })
    .catch(error => {
      console.log('[ERROR] Stop: ' + error)
    })
  }
</script>