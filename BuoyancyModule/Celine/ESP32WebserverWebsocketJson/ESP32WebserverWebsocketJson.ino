#include <WiFi.h>                                     // needed to connect to WiFi
#include <WebServer.h>                                // needed to create a simple webserver (make sure tools -> board is set to ESP32, otherwise you will get a "WebServer.h: No such file or directory" error)
#include <WebSocketsServer.h>                        // needed for instant communication between client and server through Websockets
#include <ArduinoJson.h>                              // needed for JSON encapsulation (send multiple variables with one string)
#include <ESP32Time.h>                                // needed to get real time from ESP32

// SSID and password of Wifi connection:
const char* ssid = "murex";
const char* password = "murex123";

// Instantiates ESP32's internal RTC
ESP32Time rtc(0);

// Configure IP addresses of the local access point
IPAddress local_IP(192,168,100,1);
IPAddress gateway(192,168,1,5);
IPAddress subnet(255,255,255,0);

// The String below "webpage" contains the complete HTML code that is sent to the client whenever someone connects to the webserver
String webpage = "<!DOCTYPE html><html><head><title>Page Title</title></head><body style='background-color: #EEEEEE;'><span style='color: #003366;'><h1>Time</h1><p>Time: <span id='time'>-</span></p><p><button type='button' id='BTN_SEND_BACK'>Send info to ESP32</button></p></span></body><script> var Socket; document.getElementById('BTN_SEND_BACK').addEventListener('click', button_send_back); function init() { Socket = new WebSocket('ws://' + window.location.hostname + ':81/'); Socket.onmessage = function(event) { processCommand(event); }; } function button_send_back() { var msg = {time: new Date(Date.now()).getUTCHours() + " " + new Date(Date.now()).getUTCMinutes() + " " + new Date(Date.now()).getUTCSeconds() + " "};Socket.send(JSON.stringify(msg)); } function processCommand(event) {var obj = JSON.parse(event.data);document.getElementById('time').innerHTML = obj.time; console.log(obj.time);} window.onload = function(event) { init(); }</script></html>";

// Initialization of webserver and websocket
WebServer server(80);                                 // the server uses port 80 (standard port for websites
WebSocketsServer webSocket = WebSocketsServer(81);    // the websocket uses port 81 (standard port for websockets

void setup() {
  Serial.begin(115200);                               // init serial port for debugging

  rtc.setTime(0, 0, 0, 1, 1, 2023);                   // built-in RTC random value set

  Serial.print("Setting up Access Point ... ");
  Serial.println(WiFi.softAPConfig(local_IP, gateway, subnet) ? "Ready" : "Failed!");

  Serial.print("Starting Access Point ... ");
  Serial.println(WiFi.softAP(ssid, password) ? "Ready" : "Failed!");

  Serial.print("IP address = ");
  Serial.println(WiFi.softAPIP());

  server.on("/", []() {                               // define here wat the webserver needs to do
    server.send(200, "text/html", webpage);           //    -> it needs to send out the HTML string "webpage" to the client
  });
  server.begin();                                     // start server

  webSocket.begin();                                  // start websocket
  webSocket.onEvent(webSocketEvent);                  // define a callback function -> what does the ESP32 need to do when an event from the websocket is received? -> run function "webSocketEvent()"
}

void loop() {
  server.handleClient();                              // Needed for the webserver to handle all clients
  webSocket.loop();                                   // Update function for the webSockets
  String jsonString = "";                           // create a JSON string for sending data to the client
  StaticJsonDocument<200> doc;                      // create a JSON container
  JsonObject object = doc.to<JsonObject>();         // create a JSON Object
  int timeArray[3], r = 0, t = 0;
  String time = rtc.getTime("%H:%M:%S");
  for (int i = 0; i < time.length(); i++) {
    if (time.charAt(i) == ' ') {
      timeArray[t] = time.substring(r, i).toInt();
      r = (i + 1);
      t++;
    }
  }
  object["time"] = time;
  serializeJson(doc, jsonString);                   // convert JSON object to string
  Serial.println(jsonString);                       // print JSON string to console for debug purposes
  webSocket.broadcastTXT(jsonString);               // send JSON string to clients
  delay(1000);
}

void webSocketEvent(byte num, WStype_t type, uint8_t * payload, size_t length) {      // the parameters of this callback function are always the same -> num: id of the client who send the event, type: type of message, payload: actual data sent and length: length of payload
  switch (type) {                                     // switch on the type of information sent
    case WStype_DISCONNECTED:                         // if a client is disconnected, then type == WStype_DISCONNECTED
      Serial.println("Client " + String(num) + " disconnected");
      break;
    case WStype_CONNECTED:                            // if a client is connected, then type == WStype_CONNECTED
      Serial.println("Client " + String(num) + " connected");
      // optionally you can add code here what to do when connected
      break;
    case WStype_TEXT:                                 // if a client has sent data, then type == WStype_TEXT
      // try to decipher the JSON string received
      StaticJsonDocument<200> doc;                    // create a JSON container
      DeserializationError error = deserializeJson(doc, payload);
      if (error) {
        Serial.print(F("deserializeJson() failed: "));
        Serial.println(error.f_str());
        return;
      }
      else {
        // JSON string was received correctly, so information can be retrieved:
        String time = doc["time"];
        int timeArray[3], r = 0, t = 0;
        for (int i = 0; i < time.length(); i++) {
          if (time.charAt(i) == ' ') {
            timeArray[t] = time.substring(r, i).toInt();
            r = (i + 1);
            t++;
          }
        }
        int offset = 0;
        rtc.setTime(timeArray[2] + offset, timeArray[1], timeArray[0], 1, 1, 2023);
        Serial.println("Received info from user: " + String(num));
        Serial.println("Time: " + String(time));
      }
      Serial.println("");
      break;
  }
}
