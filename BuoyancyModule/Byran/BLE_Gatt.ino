#include <BLEDevice.h>

#include <BLEUtils.h>

#include <BLEServer.h>  //Library to use BLE as server

#include <BLE2902.h>

#include <ESP32Time.h>

// Instantiates ESP32 built in RTC

ESP32Time rtc(0);

bool _BLEClientConnected = false;

std::string temp = "";

int teamNumber = 999999;

// Instantiates generic custom uuid
#define MetaDataService "1aade6e4-c95a-419f-bcd7-6ab375f19e01"

// This characteristic can be written to, read from and report notifications
BLECharacteristic MetaDataCharacteristic("fcfcad0b-035c-49e7-a828-ef109bce0682", BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_WRITE);

// BLE Server for notifications
BLEDescriptor MetaDataDescriptor(BLEUUID((uint16_t)0x2901));

class MyServerCallbacks : public BLEServerCallbacks {

  void onConnect(BLEServer* pServer) {

    _BLEClientConnected = true;
  };

  void onDisconnect(BLEServer* pServer) {

    _BLEClientConnected = false;
  }
};

void InitBLE() {

  BLEDevice::init("ESP32 Byran");

  // Create the BLE Server

  BLEServer* pServer = BLEDevice::createServer();

  pServer->setCallbacks(new MyServerCallbacks());

  // Create the BLE Service

  BLEService* pBattery = pServer->createService(MetaDataService);

  pBattery->addCharacteristic(&MetaDataCharacteristic);

  MetaDataDescriptor.setValue("Custom UUID");

  MetaDataCharacteristic.addDescriptor(&MetaDataDescriptor);

  MetaDataCharacteristic.addDescriptor(new BLE2902());

  pServer->getAdvertising()->addServiceUUID(MetaDataService);

  pBattery->start();

  // Start advertising

  pServer->getAdvertising()->start();
}

void setup() {
  // Sets baud rate to 115200
  Serial.begin(115200);

  Serial.println("UTC and Team Number Indicator - BLE");

  // Built-in RTC random value set
  rtc.setTime(0, 0, 0, 1, 1, 2023);

  // Initializes the BLE server
  InitBLE();
}

void loop() {
  if (MetaDataCharacteristic.getValue().c_str() != temp) {
    // Serial.println("Input Updated:");
    int timeArray[3], r = 0, t = 0;

    String inputFromComputer = MetaDataCharacteristic.getValue().c_str();

    // Splits string into int array
    for (int i = 0; i < inputFromComputer.length(); i++) {
      if (inputFromComputer.charAt(i) == ' ') {
        timeArray[t] = inputFromComputer.substring(r, i).toInt();
        r = (i + 1);
        t++;
      }
    }
    // Serial.println(String(timeArray[0]) + " " + String(timeArray[1]) + " " + String(timeArray[2]));

    // including manual offset of 3 from testing, should be changed depending on circumstances
    int offset = 2;

    // updates rtc time based on input from connected computer
    rtc.setTime(timeArray[2] + offset, timeArray[1], timeArray[0], 1, 1, 2023);
  }

  // Serial.println(MetaDataCharacteristic.getValue().c_str());
  std::string value = ((rtc.getTime("%H:%M:%S") + " Team Number: " + String(teamNumber)).c_str());

  temp = value;

  MetaDataCharacteristic.setValue(value);
  MetaDataCharacteristic.notify();

  // update every second
  delay(1000);
}