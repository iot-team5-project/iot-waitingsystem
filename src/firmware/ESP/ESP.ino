#include <WiFi.h>

const char *ssid = "ANE_Class2_2G";
const char *password = "addinedu_class2@";

long value1;
long value2;

WiFiServer server(80);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  // arduino uno와 통신하기 위한 시리얼
  Serial2.begin(9600);


  // wifi연결
  Serial.println("ESP32 TCP Server Start");
  Serial.println(ssid);

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

// wifi로 보내기 위한 데이터 structure
struct protocol {
  int table = 0;
  int weight = 0;
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

      // 시리얼 통신을 통해 아두이노 우노에서 센서 값 가져온다
      if(Serial2.available() >= sizeof(value1) + sizeof(value2)) {
          //Serial.println(Serial2.available());
          Serial2.readBytes((byte *)&value1, sizeof(value1));
          Serial2.readBytes((byte *)&value2, sizeof(value2));

          if (value1 < 0 ) {
            value1 = 0;
          }

          if (value2 < 0 ) {
            value2 = 0;
          }
      }

      while (client.available() > 0) {

        // python에서 신호를 보내면 다시 python으로 데이터를 보낸다
        client.readBytes(data, 8);
        memcpy(&p, &data, sizeof(p));

        if (p.table == 1)
        {
          p.weight = value1;

          memcpy(&data, &p, sizeof(p));
        }
        else if (p.table == 2)
        {
          p.weight = value2;

          memcpy(&data, &p, sizeof(p));
        }

        // Serial.println(p.table);
        // Serial.println(p.status);

        client.write(data,8);
      }

      delay(100);
    }

    client.stop();
    Serial.println("Client Disconnected!");
  }

}
