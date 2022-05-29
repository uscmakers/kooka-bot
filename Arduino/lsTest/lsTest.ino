#define SWITCH  6
#define LED     13

void setup() {
  // put your setup code here, to run once:
  pinMode(LED,OUTPUT);
  pinMode(SWITCH,INPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  while(digitalRead(SWITCH)) {digitalWrite(LED,HIGH);}
  digitalWrite(LED,LOW);
}
