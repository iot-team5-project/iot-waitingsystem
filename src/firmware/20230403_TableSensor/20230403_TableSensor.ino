#include <WiFi.h>
#include <ESP32Servo.h>
#include <PubSubClient.h>

const char *ssid = "ANE_Class2_2G";
const char *password = "addinedu_class2@";

#define mqtt_server 192.168.1.9    // your MQTT server
#define mqtt_port 1883                    // your port number
#define mqtt_topic "*****"         // your topic
#define mqtt_user "*****"               // your username (Manage User of the CloudMQTT)
#define mqtt_password "*****"             // your password (Manage User of the CloudMQTT)

const int SWITCH_PIN0 = 18; // 스위치 핀 번호
const int SWITCH_PIN1 = 19; // 스위치 핀 번호
bool switchState0 = 0; // 스위치 상태 저장 변수
bool switchState1 = 0; // 스위치 상태 저장 변수

const char *ID0 = "Switch0";  // Name of our device, must be unique
const char *ID1 = "Switch1";  // Name of our device, must be unique
const char *TOPIC0 = "Table_Message0";  // 테이블1 제어 명령 메시지를 게시할 토픽 이름
const char *TOPIC1 = "Table_Message1"; // 테이블2 제어

IPAddress broker(192,168,0,132); // IP address of your MQTT broker eg. 192.168.1.50
WiFiClient wclient;

PubSubClient client(wclient); // Setup MQTT client

void setup() {
  Serial.begin(115200); // 시리얼 통신 시작
  pinMode(SWITCH_PIN0, INPUT); // 스위치 입력 설정
  pinMode(SWITCH_PIN1, INPUT); // 스위치 입력 설정

  Serial.begin(115200);
  Serial.println("ESP32 TCP Server Start");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  while(WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.print(".");
  }
  Serial.println();

  Serial.print("IP Address :");
  Serial.println(WiFi.localIP());

  server.begin();
}

struct protocol {
  int pin = 18;
  int status = 0;
};


void loop() {
  // 스위치의 상태를 읽어와서 저장
  switchState0 = digitalRead(SWITCH_PIN0);
  switchState1 = digitalRead(SWITCH_PIN1);
  //Serial.println(switchState0);
  // 스위치가 눌렸는지 여부에 따라 출력
  WiFiClient client = server.available();
  if (client) {
    Serial.print("Client Connected : ");
    Serial.println(client.remoteIP());
    struct protocol p;
    while (client.connected()) {
      char data[8];
      while (client.available() > 0) {
        client.readBytes(data, 8);
        memcpy(&p, &data, sizeof(p));

        if (p.pin == 18)
        {
            switchState0 = digitalRead(p.pin);
            p.status = switchState0;
            Serial.println("1번 스위치가 눌렸습니다.");
        }

        else if (p.pin == 19)
        {
            switchState1 = digitalRead(p.pin);
            p.status = switchState1;
            Serial.println("2번 스위치가 눌렸습니다.");
        }

      Serial.println(p.pin);
      Serial.println(p.status);

      client.write(data, 8);
      }

      delay(10);
    }
      client.stop();
      Serial.println("Client Disconnected!");
  }
}