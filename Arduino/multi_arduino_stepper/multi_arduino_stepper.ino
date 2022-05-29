//Globals
#include <Servo.h>
#define STEPPIN 8
#define DIRPIN  7
#define SWITCH  6
#define LED     13
#define CW      0
#define CCW     1
#define INTERVAL 20
//good frequency for small motor is 1000
//good frequency for big motor is 5000
class Driver {
public:
  int frequency;
  int STEPTIME = 200;
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
    int steps = command.toFloat()/0.036;
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
  void drive(int steps)
  {
    for(int i = 0; i < steps; i++) {
      digitalWrite(STEPPIN,HIGH);
      delayMicroseconds(3);
      digitalWrite(STEPPIN,LOW);
      delayMicroseconds(STEPTIME);
    }
  }
};
Driver myDriver;
Servo myServo;
char rec;

String stuff_right = "";
int comm_right;
int timeprev = 0;
bool calStatus = 0;
void setup() {
  // put your setup code here, to run once:
  myServo.attach(9);
  pinMode(STEPPIN,OUTPUT);
  pinMode(DIRPIN,OUTPUT);
  pinMode(LED,OUTPUT);
  pinMode(SWITCH,INPUT);
  Serial.begin(115200);
  myServo.write(0);
}
void loop() {
  digitalWrite(LED,LOW);
  // put your main code here, to run repeatedly:
  while(Serial.available()){
    rec = Serial.read();
    if(rec=='x')
    {
      myDriver.handleComm(stuff_right);
      stuff_right="";
    }
    else if(rec=='c')
    {
      myServo.write(120);
      while (!digitalRead(SWITCH))
      {
        calStatus = myDriver.calibrate();
        digitalWrite(LED,HIGH);
      }
      digitalWrite(LED,LOW);
      if(calStatus) Serial.print("d");
      else Serial.print("e");
      stuff_right="";
    }
    else if(rec=='y') 
    {
      comm_right = stuff_right.toInt();
      myServo.write(2*comm_right/3);
      stuff_right="";
    }
    else
    {
      stuff_right+=rec;
    }
  }
}
