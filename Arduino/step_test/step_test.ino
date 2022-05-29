int currentMillis = 0;
int previousMillis = 0;
int interval = 50;
String stuff_right = "";
String stuff_left = "";
String comm_right = "0";
String comm2=_left = "0";
int x;
char rec;
void setup() {
  Serial.begin(115200); //initialize serial COM at 9600 baudrate

  Stepper stepper(STEPS, 8, 9, 10, 11);
  stepper.setSpeed(30);
}
void loop()
{
  currentMillis = millis();
  int time_diff = currentMillis - previousMillis;
  if (time_diff > interval){

    while(Serial.available()){
      rec = Serial.read();
      if(rec=='c'){
        break;
      }
      stuff_right+=rec;
      comm_right = stuff_right;
      stuff_right ="";
    }
    while(Serial.available()){
      rec = Serial.read();
      if(rec=='c'){
        break;
      }
      stuff_left+=rec;
      comm_left = stuff_left;
      stuff_left ="";
    }
    Serial.print(currentMillis);
    Serial.print(",");
    Serial.print(comm_right);
    Serial.print(",");
    Serial.println(comm_left);
    
   previousMillis = currentMillis;
   }

   stepper.step(comm_right);

   
}
