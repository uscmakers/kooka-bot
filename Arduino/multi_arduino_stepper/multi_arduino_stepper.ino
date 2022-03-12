//Globals
#define STEPPIN  8
#define DIRPIN   7
#define CW 0
#define CCW 1
//good frequency for small motor is 10000
//good frequency for big motor is 5000
class Driver {
public:

  int frequency;
  int STEPTIME;
  char mode;

  Driver() 
  {
    this->frequency = 5000;
    setFrequency(this->frequency);
  }
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
  void setFrequency(int freq)
  {
    this->frequency = freq;
    this->STEPTIME = 1000000/freq;
  }
  bool calibrate() 
  {
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
char rec;
String stuff_right = "";
String comm_right = "0";
int timeprev = 0;
bool calStatus = 0;
void setup() {
  // put your setup code here, to run once:
  pinMode(STEPPIN,OUTPUT);
  pinMode(DIRPIN,OUTPUT);
  Serial.begin(9600);
}
void loop() {
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
      calStatus = myDriver.calibrate();
      if(calStatus) Serial.print("d");
      else Serial.print("e");
      stuff_right="";
    }
    else
    {
      stuff_right+=rec;
    }
  }
}
