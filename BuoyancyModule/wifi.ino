#include <WiFi.h>

const char* ssid = "murex";
const char* password = "murex";

void setup() {
  Serial.begin(115200);
  delay(10);
  Serial.println('\n');
  
  WiFi.begin(ssid, password);
  Serial.print("Connecting to ");
  Serial.print(ssid);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print('.');
  }

  Serial.println('\n');
  Serial.println("Connection established!");  
  Serial.print("IP address:\t");
  Serial.println(WiFi.localIP());
}

void loop() { 

}