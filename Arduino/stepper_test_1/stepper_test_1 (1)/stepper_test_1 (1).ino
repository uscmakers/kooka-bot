//Globals
#define STEPPIN 12
#define DIRPIN 11

#define CW 0
#define CCW 1

//good frequency for small motor is 10000
//good frequency for big motor is 5000

class Driver {
private:
  int frequency;
  int STEPTIME;
  int DriverID;
  int dir;

public:
  Driver(int id, int freq, int dir)
  {
    this->DriverID = id;
    this->dir = dir;
    setFrequency(freq);
  }
  void setFrequency(int freq) 
  {
    this->frequency = freq;
    this->STEPTIME = 1000000/freq;
  }
  void accelerateForward() 
  {
    int dly = 10000;
    digitalWrite(DIRPIN,HIGH);
    delayMicroseconds(5);
    while(dly > STEPTIME) 
    {
      digitalWrite(STEPPIN,HIGH);
      delayMicroseconds(3);
      digitalWrite(STEPPIN,LOW);
      delayMicroseconds(dly);
      dly -= 10;
    }
    dir = CW;
  }
  void accelerateBackward() 
  {
    int dly = 2000;
    digitalWrite(DIRPIN,LOW);
    delayMicroseconds(5);
    while(dly > STEPTIME) 
    {
      digitalWrite(STEPPIN,HIGH);
      delayMicroseconds(3);
      digitalWrite(STEPPIN,LOW);
      delayMicroseconds(dly);
      dly -= 10;
    }
    dir = CCW;
  }
  void forward(int steps)
  {
    int i;
    digitalWrite(DIRPIN,HIGH);//SET DIRECTION
    delayMicroseconds(5);
    for(i=0;i<steps;i++){
      digitalWrite(STEPPIN,HIGH);
      delayMicroseconds(3);
      digitalWrite(STEPPIN,LOW);
      delayMicroseconds(STEPTIME);
    }
    dir = CW;
  }
  void backward(int steps)
  {
    int i;
    digitalWrite(DIRPIN,LOW);//SET DIRECTION 
    delayMicroseconds(5);
    for(i=0;i<steps;i++){
      digitalWrite(STEPPIN,HIGH);
      delay(STEPTIME);
      digitalWrite(STEPPIN,LOW);
      delay(STEPTIME);
    }
    dir = CCW;
  }
  void decelerate() 
  {
    int dly = 10000;
    if(dir == CW) digitalWrite(DIRPIN,HIGH);
    else digitalWrite(DIRPIN,LOW);
    delayMicroseconds(5);
    while(dly < STEPTIME) 
    {
      digitalWrite(STEPPIN,HIGH);
      delayMicroseconds(3);
      digitalWrite(STEPPIN,LOW);
      delayMicroseconds(dly);
      dly += 20;
    }
  }
};

Driver myDriver(0,5000,CW);

void setup() {
  // put your setup code here, to run once:
  pinMode(STEPPIN,OUTPUT);
  pinMode(DIRPIN,OUTPUT); 
  myDriver.setFrequency(5000);
  myDriver.accelerateForward();
}

void loop() {
  // put your main code here, to run repeatedly:
  //step(0);
  myDriver.forward(1);
}
