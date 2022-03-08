//Globals
//#define STEPPIN 12
//#define DIRPIN 11

#define CW 0
#define CCW 1

//good frequency for small motor is 10000
//good frequency for big motor is 5000

char rec;
String stuff_right = "";
String comm_right = "0";
int deg1 = 0;
int deg2 = 0;
int timeprev = 0;

class Driver {
private:
  int frequency;
  int STEPTIME;
  int DriverID;
  int dir;
  int STEPPIN;
  int DIRPIN;

public:
  Driver(int id, int freq, int dir, int steppin, int dirpin)
  {
    this->DriverID = id;
    this->dir = dir;
    this->STEPPIN = steppin;
    this->DIRPIN = dirpin;
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
    //int dly = 2000;
    int dly = 10000;
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
      delayMicroseconds(STEPTIME); // IT WAS THREE
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
      delayMicroseconds(STEPTIME);
      digitalWrite(STEPPIN,LOW);
      delayMicroseconds(STEPTIME);
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

Driver myDriver(0,5000,CW, 12, 11);
Driver myDriver2(0,5000,CW, 10, 9);

void setup() {
  // put your setup code here, to run once:
  pinMode(12,OUTPUT);
  pinMode(11,OUTPUT); 
  pinMode(10,OUTPUT);
  pinMode(9,OUTPUT);
  myDriver.setFrequency(10000); // small motor
  myDriver2.setFrequency(5000); // big motor
  //myDriver.accelerateBackward();
  //myDriver.accelerateForward();
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  //step(0);

  while(Serial.available()){
    rec = Serial.read();
    if(rec=='x'){
      deg1 = stuff_right.toInt();

      stuff_right ="";

    }

    else if(rec=='y'){
      deg2 = stuff_right.toInt();

      if(deg1>0 && deg2>0){
        //myDriver.forward(deg/0.036); big motor
        myDriver.forward(deg1*3/0.036); // small motor
        myDriver2.forward(deg2/0.036); // big motor

      }
      else if(deg1<0 && deg2>0){
        //myDriver.backward(abs(deg)/0.036); big motor
        myDriver.backward(abs(deg1)*3/0.036); // small motor
        myDriver2.forward(deg2/0.036); // big motor

      }
      
      else if(deg1>0 && deg2<0){
        myDriver.forward((deg1)*3/0.036); // small motor
        myDriver2.backward(abs(deg2)/0.036); // big motor
        //myDriver2.forward(deg*3/0.036); small motor

      }
      else if(deg1<0 && deg2<0){
        myDriver.backward(abs(deg1)*3/0.036); // small motor
        myDriver2.backward(abs(deg2)/0.036); // big motor
        //myDriver2.backward(abs(deg)*3/0.036); small motor

      }
      
      stuff_right ="";
      break;
    }

    else{
      stuff_right+=rec;
    }
      
  }



}
