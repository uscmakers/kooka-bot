#include <AccelStepper.h>

char rec;
String stuff_right = "";
String comm_right = "0";
int speedd = 0;

AccelStepper stepper(1,12,11);
void setup()
{
   stepper.setMaxSpeed(6000);
   //stepper.setCurrentPosition(100);
   stepper.setSpeed(0);
   Serial.begin(9600);
}
int cnt = 0;
int timeprev = 0;
void loop()
{
  //stepper.move(10);
  //stepper.runSpeed();
  if(millis() - timeprev > 100) {
    while(Serial.available()){
      rec = Serial.read();
      if(rec=='x'){
        speedd = stuff_right.toInt();
        stepper.setSpeed(speedd);
 
        stuff_right ="";
        break;
      }
      stuff_right+=rec;


    }
    
    timeprev = millis();
   }
}
