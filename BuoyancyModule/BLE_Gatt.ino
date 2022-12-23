#include <BLEDevice.h>

#include <BLEUtils.h>

#include <BLEServer.h>  //Library to use BLE as server

#include <BLE2902.h>

#include <ESP32Time.h>

ESP32Time rtc(0);

bool _BLEClientConnected = false;

#define MetaDataService "1aade6e4-c95a-419f-bcd7-6ab375f19e01"

BLECharacteristic MetaDataCharacteristic("fcfcad0b-035c-49e7-a828-ef109bce0682", BLECharacteristic::PROPERTY_READ | BLECharacteristic::PROPERTY_NOTIFY | BLECharacteristic::PROPERTY_WRITE);

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
  Serial.begin(115200);
  Serial.println("UTC and Team Number Indicator - BLE");
  rtc.setTime(59, 26, 13, 23, 12, 2022);
  InitBLE();
}

void loop() {
  // Serial.println(rtc.getTime("%H:%M:%S"));
  Serial.println(MetaDataCharacteristic.getValue().c_str());
  std::string value = ((rtc.getTime("%H:%M:%S") + " 999999").c_str());
  MetaDataCharacteristic.setValue(value);
  MetaDataCharacteristic.notify();
  delay(1000);
}