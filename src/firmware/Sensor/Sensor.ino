#include <Arduino.h>
#include "HX711.h"
#include <SoftwareSerial.h>

//set Serial communication pin
SoftwareSerial soft(3,2);  // RX : 3, TX : 2


// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 5;
const int LOADCELL_SCK_PIN = 4;
const int LOADCELL_DOUT_PIN_1 = 7;
const int LOADCELL_SCK_PIN_1 = 6;
const int f = 224450/50;
const int f1 = 184200/50;

HX711 scale ;
HX711 scale1 ;

void setup() {
  Serial.begin(9600);

  // esp에 보내주기 위해 tx ,rx 핀 설정
  soft.begin(9600);

  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale1.begin(LOADCELL_DOUT_PIN_1, LOADCELL_SCK_PIN_1);

  // 로드셀 스케일링
  scale.tare();
  scale1.tare();    
  scale.set_scale(f);
  scale1.set_scale(f1);
 
}

void loop() {

  if (scale.is_ready() & scale1.is_ready()) {
    
    // esp에 4byte 값 2개를 넘겨주기 위한 변수 
    long value1 = scale.get_units();
    long value2 = scale1.get_units();

    // // 무게 값 체크
    Serial.print("HX711_1 reading: ");
    Serial.println(value1);
    // Serial.print("HX711_2 reading: ");
    // Serial.println(value2);
.
    // esp에 시리얼 통신으로 값 보내기
    soft.write((byte*)&value1, sizeof(value1));
    soft.write((byte*)&value2, sizeof(value2));
  } 

  delay(1000);

}
