//Globals
#define STEPPIN  8
#define DIRPIN   7
#define COORDIN0 6
#define COORDIN1 5
#define COORDOUT 4
#define CW 0
#define CCW 1
//good frequency for small motor is 10000
//good frequency for big motor is 5000
class Driver {
public:

  int frequency;
  int STEPTIME;
  char mode;

  Driver() {}
  ~Driver() {}
  void init(char str) 
  {
    if(str == 'm') 
    {
      this->frequency = 5000;
    }
    else
    {
      this->frequency = 5000;
    }
    setFrequency(this->frequency);
    mode = str;
  }
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
  void setFrequency(int freq)
  {
    this->frequency = freq;
    this->STEPTIME = 1000000/freq;
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
    //coordinate();
    drive(abs(steps));
  }
  void coordinate() 
  {
    if(mode == 'm') 
    {
      digitalWrite(COORDOUT,HIGH);
      while(digitalRead(COORDIN0) == 0 || digitalRead(COORDIN1) == 0);
      digitalWrite(COORDOUT,LOW);
    }
    else 
    {
      while(digitalRead(COORDIN0) == 0);
      digitalWrite(COORDOUT,HIGH);
      while(digitalRead(COORDIN0) == 1);
      digitalWrite(COORDOUT,LOW); 
    }
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
char rec;
String stuff_right = "";
String comm_right = "0";
int timeprev = 0;
void setup() {
  // put your setup code here, to run once:
  pinMode(STEPPIN,OUTPUT);
  pinMode(DIRPIN,OUTPUT);
  pinMode(COORDIN0,INPUT);
  pinMode(COORDIN1,INPUT);
  pinMode(COORDOUT,OUTPUT);
  digitalWrite(COORDOUT,LOW);
  Serial.begin(9600);
  myDriver.init('s');
}
void loop() {
  // put your main code here, to run repeatedly:
  
  while(Serial.available()){
    rec = Serial.read();
    //if(rec=='m' || rec=='s')
    //{
    //  myDriver.init(rec);
    //}
    if(rec=='x')
    {
      myDriver.handleComm(stuff_right);
      stuff_right ="";
    }
    else
    {
      stuff_right+=rec;
    }
  }
}
