#include <SoftwareSerial.h>
int Tx = 5; //전송 보내는핀
int Rx = 4; //수신 받는핀
int baud = 9600; //보드레이트
unsigned long timestamp;
SoftwareSerial BTSerial(Tx,Rx); //RX,TX


void initAT(){    //초기 설정
  BTSerial.println("AT+RENEW");    // renew module
  delay(1000);
  BTSerial.println("AT+NOTI0");    // set notification off
  delay(1000); 
  BTSerial.println("AT+ROLE1");    // set Master(Central) mode
  delay(1000);
  BTSerial.println("AT+SHOW1");    // show name
  delay(1500);
  BTSerial.println("AT+IMME1");    // set IMME mode
  delay(1500);
  BTSerial.println("AT+RESET");    // reset module  
  delay(1500);
  BTSerial.println("AT");          // ready
  delay(1500);
}

void atCommand(String at, unsigned int time){
  if (millis() - timestamp > time*1000) {    //run every n seconds
    BTSerial.println(at); 
    timestamp = millis();
   // Serial.println(tmp);
  }
}

void setup(){
  pinMode(7,OUTPUT);    // hm10 frezzing 임시조치 -  전원공급용
  pinMode(6,OUTPUT);    // gnd
  digitalWrite(7,HIGH);
  digitalWrite(6,LOW);
  Serial.begin(baud);
  BTSerial.begin(baud);
  delay(1000);
  initAT(); 
}

void loop(){
  atCommand("AT+DISC?",5);
  if (BTSerial.available())   // Read from HM-10 and send to Serial Monitor
    Serial.write(BTSerial.read());
  if (Serial.available())    // Read from Serial Monitor and send to HM-10
    BTSerial.write(Serial.read());
}