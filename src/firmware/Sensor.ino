#include <Arduino.h>
#include "HX711.h"

// HX711 circuit wiring
const int LOADCELL_DOUT_PIN = 5;
const int LOADCELL_SCK_PIN = 4;
const int LOADCELL_DOUT_PIN_1 = 7;
const int LOADCELL_SCK_PIN_1 = 6;
const int f = 224477/50; // 아무런 큰숫자 * (터미널에 표시되는 값 / 실제 무게) , ()를 근접할때 까지 반복
const int f1 = 184200/50;

HX711 scale ;
HX711 scale1 ;

void setup() {
  Serial.begin(9600);
  scale.begin(LOADCELL_DOUT_PIN, LOADCELL_SCK_PIN);
  scale1.begin(LOADCELL_DOUT_PIN_1, LOADCELL_SCK_PIN_1);
  scale.tare();
  scale1.tare();  
  
  scale.set_scale(f);
  scale1.set_scale(f1);
  
 
}

void loop() {

  if (scale.is_ready() & scale1.is_ready()) {
    
    Serial.print("HX711 reading: ");
    Serial.println(scale.get_units());
    Serial.print("HX711_1 reading: ");
    Serial.println(scale1.get_units());
  } else {
    Serial.println("HX711 or HX711_1 not found.");
  }

  delay(1000);

}
