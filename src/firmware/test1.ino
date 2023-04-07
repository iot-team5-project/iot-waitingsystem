#include <WiFi.h>
#include <ESP32Servo.h>

const char *ssid = "ANE_Class2_2G";
const char *password = "addinedu_class2@";

Servo servo;
const int servo_pin = 5;

WiFiServer server(80);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
  Serial.println("ESP32 TCP Server Start");
  Serial.println(ssid);

  servo.attach(servo_pin);
  pinMode(21, OUTPUT);
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);

  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
  }

  Serial.println();

  Serial.print("IP address : ");
  Serial.println(WiFi.localIP());

  server.begin();

}

struct protocol {
  int pin = 21;
  int status = 0;
};

void loop() {
  // put your main code here, to run repeatedly:
  WiFiClient client = server.available();
  if (client) {
    Serial.print("Client Connected : ");
    Serial.println(client.remoteIP());
    struct protocol p;

    while (client.connected()) {
      char data[8];

      while (client.available() > 0) {
        Serial.println('a');
        client.readBytes(data, 8);
        memcpy(&p, &data, sizeof(p));
        Serial.println(data[0]);


        int value = analogRead(p.pin);
        Serial.println(value);
        p.status = value;
        memcpy(&data, &p, sizeof(p));
        Serial.println(data);
        client.write(data,8);



      }


      delay(100);
    }

    client.stop();
    Serial.println("Client Disconnected!");
  }
}