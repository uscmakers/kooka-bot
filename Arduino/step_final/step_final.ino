//Globals
#define STEPPIN0  12 //big
#define DIRPIN0   11 //big
#define STEPPIN1  10
#define DIRPIN1   9
#define STEPPIN2  8
#define DIRPIN2   7
#define CW 0
#define CCW 1
//good frequency for small motor is 10000
//good frequency for big motor is 5000
class Driver {
private:
  int DriverID;
  int stepPin;
  int dirPin;
  void init(int id, int stepPin, int dirPin)
  {
    this->DriverID = id;
    this->stepPin = stepPin;
    this->dirPin = dirPin;
  }
  void setDirection(int dir) {
    if(dir == CW)
    {
      digitalWrite(dirPin,HIGH);
    }
    else
    {
      digitalWrite(dirPin,LOW);
    }
  }
  void drive()
  {
      digitalWrite(stepPin,HIGH);
      delayMicroseconds(3);
      digitalWrite(stepPin,LOW);
  }
public:
  Driver() {}
  ~Driver() {}
  friend class parallelControl;
};
class parallelControl {
private:
  int frequency;
  int STEPTIME;
  int dir[3];
  Driver allDrivers[3];
  int stepPins[3] = {STEPPIN0,STEPPIN1,STEPPIN2};
  int dirPins[3] = {DIRPIN0,DIRPIN1,DIRPIN2};
public:
  parallelControl(int en[3], int freq)
  {
    this->setFrequency(freq);
    for(int i = 0; i<3; i++)
    {
      if(en[i] != 0)
      {
        allDrivers[i].init(i,stepPins[i],dirPins[i]);
      }
    }
  }
  ~parallelControl() {};
  void setFrequency(int freq)
  {
    this->frequency = freq;
    this->STEPTIME = 1000000/freq;
  }
  void setAllDirection(int dir[3]) 
  {
    this->dir[0] = dir[0];
    this->dir[1] = dir[1];
    this->dir[2] = dir[2];
  }
  void accelerate()
  {
    int dly = 10000;
    for(int i = 0; i<3; i++)
    {
      allDrivers[i].setDirection(dir[i]);
    }
    delayMicroseconds(5);
    while(dly > STEPTIME)
    {
      allDrivers[0].drive();
      allDrivers[1].drive();
      allDrivers[2].drive();
      delayMicroseconds(int(dly/2));
      allDrivers[1].drive();
      allDrivers[2].drive();
      delayMicroseconds(int(dly/2));
      dly -= 10;
    }
  }
  void drive(int steps[3])
  {
    int i;
    int allZero = 0;
    int notZero;
    for(int i = 0; i<3; i++)
    {
      allDrivers[i].setDirection(dir[i]);
    }
    delayMicroseconds(5);
    while (allZero == 0) {
      notZero = 0;
        if(steps[0] > 0) {
          allDrivers[0].drive();
          steps[0]--;
          notZero = 1;
        }
        if(steps[1] > 0) {
          allDrivers[1].drive();
        }
        if(steps[2] > 0) {
          allDrivers[2].drive();
        }
        delayMicroseconds(int(STEPTIME/2));
        if(steps[1] > 0) {
          allDrivers[1].drive();
          steps[1]--;
          notZero = 1;
        }
        if(steps[2] > 0) {
          allDrivers[2].drive();
          steps[2]--;
          notZero = 1;
        }
        delayMicroseconds(int(STEPTIME/2));
        if(notZero == 0)
        {
          allZero = 1;
        }
      }
    }
};
int enAll[3] = {1,1,1};
parallelControl myDrivers(enAll,5000);
char rec;
String stuff_right = "";
String comm_right = "0";
int deg[3] = {0,0,0};
int dir3[3] = {0,0,0};
int timeprev = 0;
void setup() {
  // put your setup code here, to run once:
  pinMode(STEPPIN0,OUTPUT);
  pinMode(DIRPIN0,OUTPUT);
  pinMode(STEPPIN1,OUTPUT);
  pinMode(DIRPIN1,OUTPUT);
  pinMode(STEPPIN2,OUTPUT);
  pinMode(DIRPIN2,OUTPUT);
  Serial.begin(9600);
}
void loop() {
  // put your main code here, to run repeatedly:
  while(Serial.available()){
    rec = Serial.read();
    if(rec=='x')
    {
      deg[0] = stuff_right.toInt()/0.036;
      if(deg[0] >= 0)
      {
        dir3[0] = CW;
      }
      else
      {
        dir3[0] = CCW;
      }
      deg[0] = abs(deg[0]);
      stuff_right ="";
    }
    else if(rec=='y')
    {
      deg[1] = stuff_right.toInt()/0.036;
      stuff_right ="";
      if(deg[1] >= 0)
      {
        dir3[1] = CW;
      }
      else
      {
        dir3[1] = CCW;
      }
      deg[1] = abs(deg[1]);
    }
    else if(rec=='z')
    {
      deg[2] = stuff_right.toInt()/0.036;
      if(deg[2] >= 0)
      {
        dir3[2] = CW;
      }
      else
      {
        dir3[2] = CCW;
      }
      deg[2] = abs(deg[2]);
      stuff_right ="";
      myDrivers.setAllDirection(dir3);
      myDrivers.drive(deg);
    }
    else
    {
      stuff_right+=rec;
    }
  }
}
