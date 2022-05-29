//Globals
#include <ezButton.h>
#include <Servo.h>
#define STEPPIN 8
#define DIRPIN  7
#define SWITCH  6 //
#define CW 0
#define CCW 1
#define INTERVAL 20
//good frequency for small motor is 10000
//good frequency for big motor is 5000
class Driver {
public:
  int frequency;
  int STEPTIME;
  char mode;
  Driver() {}
  ~Driver() {}
  void setDirection(int dir)
  {
    if(dir == CW)
    {
      digitalWrite(DIRPIN,HIGH);
    }
    else
    {
      digitalWrite(DIRPIN,LOW);
    }
    delayMicroseconds(5);
  }
  void setFrequency(int steps)
  {
    this->STEPTIME = 1000*INTERVAL/steps;
    this->frequency = 1000000/STEPTIME;
  }
  void drive(int steps)
  {
    for(int i = 0; i < steps; i++) {
      digitalWrite(STEPPIN,HIGH);
      delayMicroseconds(3);
      digitalWrite(STEPPIN,LOW);
      delayMicroseconds(STEPTIME);
    }
  }
  int calibrate()
  {
    for(int i = 0; i < 5; i++)
    {
      digitalWrite(STEPPIN,HIGH);
      delayMicroseconds(3);
      digitalWrite(STEPPIN,LOW);
      delayMicroseconds(STEPTIME);
      }
     return true;
  }
  void handleComm(String command)
  {
    int steps = command.toInt()/0.036;
    if(steps >= 0)
    {
      setDirection(CW);
    }
    else
    {
      setDirection(CCW);
    }
    setFrequency(abs(steps));
    drive(abs(steps));
  }
};
Driver myDriver;
Servo myServo;
char rec;
String stuff_right = "";
String comm_right = "0";
int timeprev = 0;
bool calStatus = 0;
ezButton limitSwitch(SWITCH);
void setup() {
  // put your setup code here, to run once:
  pinMode(STEPPIN,OUTPUT);
  pinMode(DIRPIN,OUTPUT);
  Serial.begin(115200);
  limitSwitch.setDebounceTime(50);
}
void loop() {
  // put your main code here, to run repeatedly:
  limitSwitch.loop();
  while(Serial.available()){
    rec = Serial.read();
    if(rec=='x')
    {
      myDriver.handleComm(stuff_right);
      stuff_right="";
    }
    else if(rec=='c')
    {
      while (!limitSwitch.isPressed())
      {
        Serial.println(limitSwitch.isPressed());
        calStatus = myDriver.calibrate();
      }
      Serial.println(limitSwitch.isPressed());
      if(calStatus) Serial.print("d");
      else Serial.print("e");
      stuff_right="";
    }
    else if(rec=='y')
    {
      
    }
    else
    {
      stuff_right+=rec;
    }
  }
}
