# 맛집 waiting 알리미
![image](https://github.com/iot-team5-project/iot-waitingsystem/assets/124905739/a5b8b9e9-bbbc-4eb5-b698-21779bcbf7de)
# 조원 역할
![image](https://github.com/iot-team5-project/iot-waitingsystem/assets/124905739/ca2b8f96-27bf-4080-82d7-dd4e8137cc6b)
# 코드 동작 설명 
- Sensor.ino
  - arduino에서 무게 센서를 통해 무게 측정하고 esp32로 무게값을 보낸다.
- ESP.ino
  - arduino에서 받은 무게값 저장한다.
  - TCP 서버를 만들고 wifi연결을 통해 client에서 신호를 받으면 저장된 무게값 전달한다.
![table](https://github.com/iot-team5-project/iot-waitingsystem/assets/124905739/7d104228-55b3-473a-89eb-beff336a4099)
- rest_control.py
  - 예약, 대기자 현황, 테이블의 식사상황을 보여준다
  - 테이블에 올려진 음식 무게를 통해 대략적인 식사 상황을 보여준다.
![image](https://github.com/iot-team5-project/iot-waitingsystem/assets/124905739/ab9c3411-7f20-4c68-aa55-38fd04543c89)
