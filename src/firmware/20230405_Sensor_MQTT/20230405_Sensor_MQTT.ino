#include <WiFi.h>
#include <PubSubClient.h>

// WiFi 연결 정보
const char *ssid = "ANE_Class2_2G";
const char *password = "addinedu_class2@";

// MQTT 브로커 정보
const char* mqtt_server = "192.168.0.32";
const int mqtt_port = 1883;

// MQTT 클라이언트
WiFiClient espClient;
PubSubClient client(espClient);

// 스위치 핀
const int switch1_pin = 18;
const int switch2_pin = 19;
bool switch1_status = HIGH;  // Assume switch is not pressed, i.e. HIGH
bool switch2_status = HIGH;  // Assume switch is not pressed, i.e. HIGH

void setup() {
  Serial.begin(115200);
  pinMode(switch1_pin, INPUT_PULLUP);
  pinMode(switch2_pin, INPUT_PULLUP);

  // WiFi 연결
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }

  Serial.println("Connected to WiFi");

  // MQTT 연결
  client.setServer(mqtt_server, mqtt_port);
}

void loop() {
  switch1_status = digitalRead(switch1_pin);
  switch2_status = digitalRead(switch2_pin);
  Serial.println("Switch 1: " + String(switch1_status));
  Serial.println("Switch 2: " + String(switch2_status));
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

void reconnect() {
  while (!client.connected()) {
    Serial.println("Connecting to MQTT broker...");
    if (client.connect("ESP32Client")) {
      Serial.println("Connected to MQTT broker");
    } else {
      Serial.print("Failed to connect to MQTT broker, rc=");
      Serial.print(client.state());
      Serial.println(" retrying in 5 seconds");
      delay(5000);
    }
  }
}